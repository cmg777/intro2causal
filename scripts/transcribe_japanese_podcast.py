"""Transcribe actual Japanese TTS chunks, verify coverage, and align readable script sentences."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import difflib
from decimal import Decimal
import hashlib
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time
import threading
import unicodedata
import wave
sys.path.insert(0, str(Path(__file__).resolve().parent))
from japanese_podcast_audio import ROOT, PRODUCTION, LEDGER, CACHE, RATE, Budget, atomic_json, api_key, production_lock, sha


def canonical_numbers(text):
    text = unicodedata.normalize('NFKC', text).replace(',', '')
    text = re.sub(r'(\d+)\s*/\s*(\d+)', lambda m: m[2] + '分の' + m[1], text)
    text = re.sub(r'(\d+(?:\.\d+)?)万(\d*)',
                  lambda m: str(Decimal(m[1]) * 10000 + Decimal(m[2] or '0')).removesuffix('.0'), text)
    return text


def normalized(text):
    text = canonical_numbers(text)
    # Equivalent written/phonetic forms of the chapter's named school. This does
    # not normalize substantive different words such as arrest versus dropout.
    text = re.sub(r'Knowledge\s*Is\s*Power\s*Program', 'ナレッジイズパワープログラム', text, flags=re.I)
    text = re.sub(r'(?<![A-Za-z])KIPP(?![A-Za-z])|切符', 'キップ', text, flags=re.I)
    text = re.sub(r'first\s*stage', 'ファーストステージ', text, flags=re.I)
    return ''.join(c for c in text.casefold()
                   if unicodedata.category(c)[0] in ('L', 'N'))


def offset_seconds(value):
    if hasattr(value, 'total_seconds'):
        return value.total_seconds()
    if isinstance(value, (float, int)):
        return float(value)
    match = re.fullmatch(r'(\d+(?:\.\d+)?)s', str(value))
    if match:
        return float(match[1])
    raise ValueError(f'Unrecognized timestamp format: {type(value).__name__}')


def stamp(value):
    milliseconds = round(value * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'


def number_flags(expected, heard):
    heard = canonical_numbers(heard)
    flags = []
    for match in re.finditer(r'\d+(?:,\d{3})*(?:\.\d+)?', expected):
        number = match[0].replace(',', '')
        significant = '.' in number or float(number) >= 10 or expected[match.end():].startswith('パーセント')
        if significant and not re.search(r'(?<![\d.])' + re.escape(number) + r'(?![\d.])', heard):
            if match[0] not in flags:
                flags.append(match[0])
    return flags


def response_words(response, duration):
    if not response.get('candidates') or str(response['candidates'][0].get('finish_reason')).split('.')[-1] != 'STOP':
        raise ValueError('Incomplete speech-recognition response')
    words, omitted = [], []
    raw_words = [word for candidate in response['candidates']
                 for part in candidate.get('content', {}).get('parts', [])
                 for word in part.get('audio_transcription', {}).get('words', [])]
    if not raw_words:
        raise ValueError('Provider returned no word timestamps; raw response retained for explicit retry review')
    for index, word in enumerate(raw_words):
        start, end = offset_seconds(word['start_offset']), offset_seconds(word['end_offset'])
        if not 0 <= start <= end <= duration + .5 or (words and start < words[-1]['start']):
            omitted.append({'index': index, 'word': word['word'], 'start': start, 'end': end,
                            'reason': 'Invalid provider timing; anchor omitted, no replacement time invented'})
            continue
        words.append({'word': word['word'], 'start': start, 'end': min(duration, end)})
    if not words or len(omitted) > 2 or len(omitted) / max(1, len(raw_words)) > .01:
        raise ValueError('Too many invalid recognition timing anchors; raw response retained for review')
    return words, omitted


def preserve_empty_response_for_retry(raw_path, raw, config):
    candidates = raw.get('candidates', [])
    parts = [p for c in candidates for p in c.get('content', {}).get('parts', [])]
    empty = (candidates and parts and all(str(c.get('finish_reason')).split('.')[-1] == 'STOP' for c in candidates)
             and all(set(p) == {'text'} and p['text'] == '' for p in parts))
    if not empty or config.get('recognition_empty_retry_limit', 0) != 1:
        return False
    archived = raw_path.with_name(raw_path.name.replace('.recognition-response.json', '.recognition-empty-response-attempt1.json'))
    if archived.exists():
        raise ValueError('Empty ASR response after the one permitted retry; both attempts retained')
    raw_path.rename(archived)
    print('Empty ASR response retained; allowing one budgeted retry for ' + raw_path.name[:10], flush=True)
    return True


def recover_recognition(path, duration, config, budget):
    raw_path = path.with_suffix('.recognition-response.json')
    if not raw_path.exists():
        return None
    raw = json.loads(raw_path.read_text())
    if preserve_empty_response_for_retry(raw_path, raw, config):
        return None
    words, omitted = response_words(raw, duration)
    # The raw file is written by the latest request for this exact chunk.
    ledger = json.loads(LEDGER.read_text())
    requests = [r for r in ledger['requests'] if r['cache_key'] == path.stem + ':recognition']
    latest = requests[-1] if requests else None
    usage = raw.get('usage_metadata', {})
    if latest and latest['status'] == 'reserved':
        budget.settle(latest, usage.get('prompt_token_count'), usage.get('candidates_token_count'), 0)
    result = {'pcm_sha256': sha(path), 'model': config['model'], 'words': words,
              'request_id': latest['id'] if latest else None,
              'omitted_timing_anchors': omitted, 'recovered_from_cached_raw_response': True}
    atomic_json(path.with_suffix('.recognition.json'), result)
    return result


def recognize(client, path, duration, config):
    from google.genai import types
    pcm = path.read_bytes()
    stream = io.BytesIO()
    with wave.open(stream, 'wb') as wav:
        wav.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        wav.writeframes(pcm)
    response = client.models.generate_content(model='gemini-3.5-transcribe',
        contents=[types.Part.from_bytes(data=stream.getvalue(), mime_type='audio/wav')],
        config=types.GenerateContentConfig(max_output_tokens=8192,
            audio_transcription_config=types.AudioTranscriptionConfig(language_codes=['ja-JP'], word_timestamp=True)))
    raw = response.model_dump(mode='json',exclude_none=True)
    atomic_json(path.with_suffix('.recognition-response.json'), raw)
    words, omitted = response_words(raw, duration)
    usage = response.usage_metadata
    return words, getattr(usage, 'prompt_token_count', None), getattr(usage, 'candidates_token_count', None), omitted


class RecognitionRateLimiter:
    def __init__(self):
        self.lock, self.next_start = threading.Lock(), 0.

    def wait(self, stop):
        with self.lock:
            if stop.wait(max(0., self.next_start - time.monotonic())):
                raise ValueError('Recognition batch stopped after another chunk failed')
            self.next_start = time.monotonic() + 20


def recognition_for_chunk(client, pcm, duration, config, budget, limiter=None, stop=None):
    recovered = recover_recognition(pcm, duration, config, budget)
    if recovered:
        return recovered
    for attempt in range(2):
        if stop and stop.is_set():
            raise ValueError('Recognition batch stopped after another chunk failed')
        if limiter:
            limiter.wait(stop)
        reservation = budget.reserve('', 8192, pcm.stem + ':recognition',
            input_token_bound=math.ceil(duration * 25) + 4096)
        try:
            words, inputs, outputs, omitted = recognize(client, pcm, duration, config)
        except ValueError:
            raw_path = pcm.with_suffix('.recognition-response.json')
            if raw_path.exists() and preserve_empty_response_for_retry(raw_path, json.loads(raw_path.read_text()), config):
                time.sleep(20)
                continue
            raise
        budget.settle(reservation, inputs, outputs, 0)
        result = {'pcm_sha256': sha(pcm), 'model': config['model'], 'words': words,
                  'request_id': reservation['id'], 'omitted_timing_anchors': omitted}
        atomic_json(pcm.with_suffix('.recognition.json'), result)
        return result
    raise ValueError('Recognition retry limit reached; successful caches retained')


def prefetch_recognition(stem, config, budget, workers):
    from google import genai
    from google.genai import types
    audio = ROOT / 'mindmaps-podcast/ja/audio' / (stem + '.mp3')
    synthesis = json.loads(audio.with_suffix('.json').read_text())
    if sha(audio) != synthesis['audio_sha256']:
        raise ValueError('Audio changed before recognition batch')
    pending, seen = [], set()
    for chunk in synthesis['timeline']:
        key = chunk['cache_key']
        if key in seen:
            continue
        seen.add(key)
        pcm = CACHE / stem / (key + '.pcm')
        meta = json.loads(pcm.with_suffix('.json').read_text())
        if sha(pcm) != meta['pcm_sha256']:
            raise ValueError('Corrupt TTS chunk before recognition batch')
        if not pcm.with_suffix('.recognition.json').exists():
            pending.append((pcm, meta['duration_seconds']))
    limiter, stop = RecognitionRateLimiter(), threading.Event()
    def run(item):
        pcm, duration = item
        client = genai.Client(api_key=api_key(), http_options=types.HttpOptions(timeout=180000,
            retry_options=types.HttpRetryOptions(attempts=1)))
        try:
            recognition_for_chunk(client, pcm, duration, config, budget, limiter, stop)
            print(f'Recognized completed audio chunk {pcm.stem[:10]} ({duration:.1f}s)', flush=True)
        finally:
            client.close()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run, item) for item in pending]
        try:
            for future in as_completed(futures):
                future.result()
        except Exception:
            stop.set()
            for future in futures:
                future.cancel()
            raise


def align_chunk(chunk, words):
    if not words:
        raise ValueError('Speech recognition returned no word timestamps')
    heard, times = '', []
    for word in words:
        text = normalized(word['word'])
        heard += text
        times.extend(word['start'] + (word['end'] - word['start']) * i / max(1, len(text)) for i in range(len(text)))
    expected = ''.join(normalized(t['text']) for t in chunk['turns'])
    matcher = difflib.SequenceMatcher(None, expected, heard, autojunk=False)
    anchors = {}
    for block in matcher.get_matching_blocks():
        for i in range(block.size):
            anchors[block.a + i] = times[block.b + i]
    coverage = len(anchors) / max(1, len(expected))
    if coverage < .8:
        raise ValueError(f'Only {coverage:.1%} recognized script coverage; inspect this audio chunk')
    length = chunk['end_seconds'] - chunk['start_seconds']
    def locate(index):
        left = max((a for a in anchors if a <= index), default=-1)
        right = min((a for a in anchors if a >= index), default=len(expected))
        if left == right:
            return anchors[left]
        a, b = anchors.get(left, 0.), anchors.get(right, length)
        return a + (b - a) * (index - left) / (right - left)
    segments, cursor = [], 0
    for turn in chunk['turns']:
        sentences = re.findall(r'.+?(?:[。！？](?:[」』])?|$)', turn['text'])
        for sentence in sentences:
            start = max(0., min(length, locate(cursor)))
            units = len(normalized(sentence))
            local_match = sum(cursor <= a < cursor + units for a in anchors) / max(1, units)
            if local_match < .5:
                raise ValueError(f'Unmatched sentence requires review: {sentence[:40]}')
            segments.append({'start': round(chunk['start_seconds'] + start, 3),
                             'end': round(chunk['end_seconds'], 3), 'speaker': turn['speaker'],
                             'section': turn['section'], 'text': sentence})
            cursor += units
    for i in range(len(segments) - 1):
        segments[i]['end'] = segments[i + 1]['start']
    if any(s['start'] >= s['end'] for s in segments):
        raise ValueError('Invalid sentence boundary from recognition; review before publishing')
    flags = []
    for opcode, a, b, c, d in matcher.get_opcodes():
        if opcode != 'equal' and b - a >= 10:
            flags.append({'expected': expected[a:b], 'recognized': heard[c:d],
                          'start_seconds': round(chunk['start_seconds'] + locate(a), 2)})
    recognized = ''.join(w['word'] for w in words)
    return segments, {'matched_characters': round(coverage, 4), 'flags': flags,
                      'number_flags': number_flags(''.join(t['text'] for t in chunk['turns']), recognized),
                      'recognized_text': recognized}


def watch_recognition(stem):
    from google import genai
    from google.genai import types
    production = json.loads(PRODUCTION.read_text())
    config = {**production, 'model': 'gemini-3.5-transcribe', 'pricing': {
        'checked_at': '2026-10-23', 'valid_through': '2026-12-31',
        'input_usd_per_million': 2., 'output_usd_per_million': 12.,
        'audio_tokens_per_second': 0, 'source': 'https://ai.google.dev/gemini-api/docs/pricing'}}
    client = genai.Client(api_key=api_key(), http_options=types.HttpOptions(timeout=180000,
        retry_options=types.HttpRetryOptions(attempts=1)))
    budget, last_progress = Budget(LEDGER, config), time.monotonic()
    workers = production.get('recognition_workers', 1)
    if workers not in (1, 2):
        raise ValueError('Recognition workers must be one or two')
    if workers > 1 and (ROOT / 'mindmaps-podcast/ja/audio' / (stem + '.json')).exists():
        client.close()
        prefetch_recognition(stem, config, budget, workers)
        return
    while True:
        for meta_path in sorted((CACHE / stem).glob('*.json')):
            if not re.fullmatch(r'[a-f0-9]{64}', meta_path.stem):
                continue
            pcm = meta_path.with_suffix('.pcm')
            destination = pcm.with_suffix('.recognition.json')
            if destination.exists() or not pcm.exists():
                continue
            meta = json.loads(meta_path.read_text())
            if sha(pcm) != meta['pcm_sha256']:
                raise ValueError('Corrupt TTS chunk before recognition')
            duration = meta['duration_seconds']
            if recover_recognition(pcm, duration, config, budget):
                last_progress = time.monotonic()
                continue
            recognition_for_chunk(client, pcm, duration, config, budget)
            last_progress = time.monotonic()
            print(f'Recognized completed audio chunk {meta_path.stem[:10]} ({duration:.1f}s)', flush=True)
            # Pace requests conservatively for account-level per-minute quotas.
            time.sleep(20)
        report = ROOT / 'mindmaps-podcast/ja/audio' / f'{stem}.json'
        if report.exists():
            plan = json.loads(report.read_text())['timeline']
            if all((CACHE / stem / (c['cache_key'] + '.recognition.json')).exists() for c in plan):
                return
        if time.monotonic() - last_progress > 240:
            raise ValueError('No new audio for four minutes; recognition cache saved for resume')
        time.sleep(5)


def build(stem, cached_only=False):
    from google import genai
    from google.genai import types
    production = json.loads(PRODUCTION.read_text())
    audio = ROOT / 'mindmaps-podcast/ja/audio' / f'{stem}.mp3'
    synthesis = json.loads(audio.with_suffix('.json').read_text())
    if synthesis['audio_sha256'] != sha(audio):
        raise ValueError('Audio changed after synthesis report')
    reviewed_path = ROOT / 'mindmaps-podcast/ja/transcripts' / (stem + '.json')
    if reviewed_path.exists():
        previous = json.loads(reviewed_path.read_text())
        source = ROOT / 'mindmaps-podcast/ja' / (stem + '.md')
        if ((previous.get('flag_review_complete') or previous.get('number_review_complete'))
            and previous.get('audio_sha256') == synthesis['audio_sha256']
            and previous.get('script_sha256') == sha(source)
            and not previous.get('unreviewed_flagged_spans', 0)
            and not previous.get('unreviewed_number_flags', 0)
            and all(reviewed_path.with_suffix(ext).exists() for ext in ('.txt', '.vtt'))):
            print(f'{stem}: current editorially reviewed transcript preserved; no API requests sent')
            return
    config = {**production, 'model': 'gemini-3.5-transcribe', 'pricing': {
        'checked_at': '2026-10-23', 'valid_through': '2026-12-31',
        'input_usd_per_million': 2.0, 'output_usd_per_million': 12.0,
        'audio_tokens_per_second': 0, 'source': 'https://ai.google.dev/gemini-api/docs/pricing'}}
    budget = Budget(LEDGER, config)
    client, segments, reports = None, [], []
    for i, chunk in enumerate(synthesis['timeline']):
        pcm = CACHE / stem / (chunk['cache_key'] + '.pcm')
        recognition_path = pcm.with_suffix('.recognition.json')
        if recognition_path.exists():
            recognition = json.loads(recognition_path.read_text())
            if recognition['pcm_sha256'] != sha(pcm):
                raise ValueError('Stale recognition cache')
        else:
            if cached_only:
                raise ValueError('Cached-only rendering requires every recognition chunk; no API request sent')
            duration = chunk['end_seconds'] - chunk['start_seconds']
            recognition = recover_recognition(pcm, duration, config, budget)
        if not recognition_path.exists():
            if client is None:
                client = genai.Client(api_key=api_key(), http_options=types.HttpOptions(timeout=180000,
                    retry_options=types.HttpRetryOptions(attempts=1)))
            duration = chunk['end_seconds'] - chunk['start_seconds']
            recognition = recognition_for_chunk(client, pcm, duration, config, budget)
        aligned, report = align_chunk(chunk, recognition['words'])
        reports.append({'chunk': i + 1, **report,
                        'recognition_model': recognition.get('model', 'unknown'),
                        'timing_granularity': recognition.get('timing_granularity', 'word timestamps'),
                        'timing_fallback': recognition.get('timing_fallback'),
                        'omitted_timing_anchors': recognition.get('omitted_timing_anchors', [])})
        segments.extend(aligned)
        print(f'{stem} chunk {i + 1}: {report["matched_characters"]:.1%} script matched; '
              f'{len(report["flags"])} span(s) flagged', flush=True)
    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=nw=1:nk=1', str(audio)], text=True))
    output = ROOT / 'mindmaps-podcast/ja/transcripts'
    output.mkdir(parents=True, exist_ok=True)
    sections, previous = [], None
    for i, segment in enumerate(segments):
        if segment['section'] != previous:
            sections.append({'title': segment['section'], 'start': segment['start'], 'segment': i})
            previous = segment['section']
    source = ROOT / 'mindmaps-podcast/ja' / f'{stem}.md'
    flags = sum(len(r['flags']) for r in reports)
    numeric_flags = sum(len(r['number_flags']) for r in reports)
    report = {'title': source.read_text().splitlines()[0].removeprefix('# '), 'duration': duration,
              'audio_sha256': sha(audio), 'script_sha256': sha(source), 'sections': sections,
              'segments': segments, 'alignment': reports, 'unreviewed_flagged_spans': flags,
              'unreviewed_number_flags': numeric_flags,
              'timing': 'Script sentences aligned to recognized audio timestamps; approximate timing. Source and granularity are recorded per chunk.',
              'verification': 'ASR comparison; flagged spans require review; not a claim of human listening'}
    atomic_json(output / f'{stem}.json', report)
    text = [report['title'], '', 'AI音声。文字起こしの時刻は近似です。', '']
    vtt = ['WEBVTT', '']
    for i, segment in enumerate(segments):
        label = '司会' if segment['speaker'] == 'HOST' else '先生'
        text.extend([f'[{stamp(segment["start"])}] {label}：{segment["text"]}', ''])
        vtt.extend([str(i + 1), f'{stamp(segment["start"])} --> {stamp(segment["end"])}',
                    f'<v {label}>{segment["text"]}', ''])
    (output / f'{stem}.txt').write_text('\n'.join(text))
    (output / f'{stem}.vtt').write_text('\n'.join(vtt))
    print(f'{stem}: {len(segments)} aligned sentences; {flags} long spans and {numeric_flags} numbers to review')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stem')
    parser.add_argument('--watch', action='store_true', help='Recognize finished chunks while synthesis continues')
    parser.add_argument('--cached-only', action='store_true', help='Render completed recognition caches without API requests')
    args = parser.parse_args()
    if not re.fullmatch(r'(?:ch0[1-6]-[a-z-]+|voice-sample)', args.stem):
        parser.error('Use a Japanese episode stem or voice-sample')
    if args.watch and args.cached_only:
        parser.error('--watch and --cached-only cannot be combined')
    try:
        with production_lock('render-' + args.stem if args.cached_only else 'recognition'):
            if args.watch:
                watch_recognition(args.stem)
            build(args.stem, cached_only=args.cached_only)
    except Exception as exc:
        if isinstance(exc, (ValueError, FileNotFoundError)):
            parser.exit(1, f'Stopped: {exc}\n')
        if getattr(exc, 'code', None) == 429:
            details = json.dumps(getattr(exc, 'details', None), default=str)
            quotas = re.findall(r'"quotaId"\s*:\s*"([A-Za-z0-9_]+)"', details)
            delays = re.findall(r'"retryDelay"\s*:\s*"([0-9.s]+)"', details)
            print(f'Quota identifiers: {quotas}; retry delays: {delays}', flush=True)
        parser.exit(1, f'Stopped: {type(exc).__name__}; HTTP {getattr(exc,"code",None)}; ledger retained\n')
