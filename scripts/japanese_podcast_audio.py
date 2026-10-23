#!/usr/bin/env python3
"""Resumable Japanese Gemini TTS with an on-disk spending ledger and sample gate."""
import argparse
from contextlib import contextmanager
from datetime import date, datetime, timezone
import fcntl
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import wave

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / 'publishing/spotify-jpn/production.json'
LEDGER = ROOT / 'publishing/spotify-jpn/gemini-usage.json'
CACHE = ROOT / '.work/podcast-ja'
RATE = 24000


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_units(text):
    # Counts Unicode characters rather than English whitespace-delimited words.
    return len(re.sub(r'\s', '', text))


def parse_script(path):
    turns, section = [], ''
    for number, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('# ') or line.startswith('Two voices:'):
            continue
        if line.startswith('## '):
            section = line[3:]
            continue
        match = re.fullmatch(r'(HOST|ECONOMIST): (.+)', line)
        if not match:
            raise ValueError(f'Unexpected script text at line {number}')
        if not section:
            raise ValueError('Turns must be under a section heading')
        speaker, text = match.groups()
        if not re.search(r'[ぁ-んァ-ヶ一-龯]', text):
            raise ValueError(f'No Japanese in line {number}')
        if turns and turns[-1]['speaker'] == speaker:
            raise ValueError(f'Nonalternating speakers at line {number}')
        if re.search(r'https?://|\*\*|`|\$|<[^>]+>', text):
            raise ValueError(f'Unspoken markup in line {number}')
        turns.append({'speaker': speaker, 'text': text, 'section': section})
    if not turns or {t['speaker'] for t in turns} != {'HOST', 'ECONOMIST'}:
        raise ValueError('Expected a nonempty two-speaker Japanese dialogue')
    return turns


def split_text(text, maximum):
    sentences = re.findall(r'.+?(?:[。！？](?:[」』])?|$)', text)
    result, current = [], ''
    for sentence in sentences:
        if text_units(sentence) > maximum:
            raise ValueError('Single sentence exceeds chunk limit; shorten the sentence before TTS')
        if current and text_units(current + sentence) > maximum:
            result.append(current)
            current = ''
        current += sentence
    if current:
        result.append(current)
    if ''.join(result) != text:
        raise ValueError('Sentence splitting would drop text')
    return result


def chunk_turns(turns, maximum=650):
    plan, current, size = [], [], 0
    for turn in turns:
        for piece in split_text(turn['text'], maximum):
            count = text_units(piece)
            if current and (size + count > maximum or turn['section'] != current[-1]['section']):
                plan.append(current)
                current, size = [], 0
            current.append({**turn, 'text': piece})
            size += count
    if current:
        plan.append(current)
    return plan


def verify_audits(script, directory):
    expected = {'content': ['C' + str(i) for i in range(1, 6)],
                'pedagogy': ['P' + str(i) for i in range(1, 8)],
                'clarity': ['L' + str(i) for i in range(1, 6)]}
    for lens, criteria in expected.items():
        record = json.loads((directory / f'{lens}.json').read_text())
        if record.get('script_sha256') != sha(script):
            raise ValueError(f'Stale {lens} audit')
        for criterion in criteria:
            score = record['scores'][criterion]
            if not 4 <= score['score'] <= 5 or not score.get('reason'):
                raise ValueError(f'Failed/incomplete audit: {lens} {criterion}')
        if any(f.get('severity') in ('error', 'major') and f.get('status', 'open') == 'open'
               for f in record.get('findings', [])):
            raise ValueError(f'Open major/error in {lens} audit')


class Budget:
    def __init__(self, path, production):
        self.path, self.production = path, production
        self.data = json.loads(path.read_text()) if path.exists() else {
            'schema_version': 1, 'project_id': 'intro2causal-ja', 'requests': []}
        if self.data.get('project_id') != 'intro2causal-ja':
            raise ValueError('Usage ledger belongs to another project')

    @property
    def committed(self):
        return sum(r.get('charged_estimate_usd', r['reserved_usd']) for r in self.data['requests'])

    def reserve(self, text, max_output, cache_key, input_token_bound=None):
        with production_lock('budget'):
            if self.path.exists():
                self.data = json.loads(self.path.read_text())
            return self._reserve(text, max_output, cache_key, input_token_bound)

    def _reserve(self, text, max_output, cache_key, input_token_bound=None):
        pricing = self.production['pricing']
        if date.today() > date.fromisoformat(pricing['valid_through']):
            raise ValueError('Refresh current Gemini pricing before new requests')
        # UTF-8 byte count + generous framing margin upper-bounds text tokens conservatively.
        input_bound = input_token_bound if input_token_bound is not None else len(text.encode('utf-8')) + 4096
        amount = (input_bound * pricing['input_usd_per_million'] +
                  max_output * pricing['output_usd_per_million']) / 1_000_000
        if self.committed + amount > self.production['gemini_budget_usd']:
            raise ValueError('Next request would exceed the US$25 Gemini budget; no request sent')
        record = {'id': len(self.data['requests']) + 1, 'cache_key': cache_key,
                  'created_at': datetime.now(timezone.utc).isoformat(), 'reserved_usd': amount,
                  'input_token_bound': input_bound, 'max_output_tokens': max_output,
                  'status': 'reserved', 'model': self.production['model'], 'pricing': pricing}
        self.data['requests'].append(record)
        atomic_json(self.path, self.data)
        return record

    def settle(self, record, input_tokens, output_tokens, seconds):
        with production_lock('budget'):
            self.data = json.loads(self.path.read_text())
            current = next(r for r in self.data['requests'] if r['id'] == record['id'])
            return self._settle(current, input_tokens, output_tokens, seconds)

    def _settle(self, record, input_tokens, output_tokens, seconds):
        price = record['pricing']
        audio_tokens = max(output_tokens or 0, math.ceil(seconds * price['audio_tokens_per_second']))
        # Missing usage remains conservatively reserved instead of assumed free.
        if input_tokens is not None and output_tokens is not None:
            amount = (input_tokens * price['input_usd_per_million'] +
                      audio_tokens * price['output_usd_per_million']) / 1_000_000
            if input_tokens > record['input_token_bound'] or audio_tokens > record['max_output_tokens']:
                record.update(status='usage_bound_exceeded', charged_estimate_usd=max(amount, record['reserved_usd']))
                atomic_json(self.path, self.data)
                raise ValueError('Provider exceeded the reserved usage bound; stopped for review')
            record['charged_estimate_usd'] = amount
        record.update(status='completed', input_tokens=input_tokens, output_tokens=output_tokens,
                      duration_seconds=seconds)
        atomic_json(self.path, self.data)


@contextmanager
def production_lock(name='generation'):
    CACHE.mkdir(parents=True, exist_ok=True)
    with (CACHE / f'{name}.lock').open('a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | (0 if name == 'budget' else fcntl.LOCK_NB))
        except BlockingIOError as exc:
            raise ValueError(f'Another Japanese {name} operation is active') from exc
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def api_key():
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ['GEMINI_API_KEY']
    result = subprocess.run(['security', 'find-generic-password', '-a', os.environ.get('USER', ''),
                             '-s', 'GEMINI_API_KEY', '-w'], capture_output=True, text=True)
    if result.returncode or not result.stdout.strip():
        raise ValueError('GEMINI_API_KEY is unavailable in environment or existing Keychain item')
    return result.stdout.strip()


def normalize_audio(data, mime):
    if data[:4] == b'RIFF':
        with wave.open(io.BytesIO(data), 'rb') as wav:
            if (wav.getframerate(), wav.getsampwidth(), wav.getnchannels()) != (RATE, 2, 1):
                raise ValueError('Unexpected Gemini WAV format')
            pcm = wav.readframes(wav.getnframes())
            if len(pcm) != wav.getnframes() * 2:
                raise ValueError('Truncated WAV')
    elif mime and ('pcm' in mime or 'L16' in mime):
        pcm = data
    else:
        raise ValueError('Unrecognized Gemini audio encoding')
    if not pcm or len(pcm) % 2:
        raise ValueError('Empty or incomplete PCM')
    return pcm


def spoken(text):
    # Decimal digits are read individually, not as a whole integer after the point.
    numerals = dict(zip('0123456789', '零一二三四五六七八九'))
    text = re.sub(r'\d+\.\d+', lambda m: m[0].split('.')[0] + '点' +
                  ''.join(numerals[x] for x in m[0].split('.')[1]), text)
    pronunciation = ROOT / 'publishing/spotify-jpn/pronunciation.json'
    if pronunciation.exists():
        mapping = json.loads(pronunciation.read_text())
        for word in sorted(mapping, key=len, reverse=True):
            pattern = re.escape(word)
            if word.isascii():
                pattern = r'(?<![A-Za-z0-9])' + pattern + r'(?![A-Za-z0-9])'
            text = re.sub(pattern, lambda match: mapping[word], text)
    return text


def synthesize(client, turns, production):
    from google.genai import types
    parts = [types.Part(text=spoken(t['text']), speech_metadata=types.SpeechMetadata(
        speaker=t['speaker'], style=production['style'][t['speaker']])) for t in turns]
    response = client.models.generate_content(model=production['model'], contents=[
        types.Content(role='user', parts=parts)], config=types.GenerateContentConfig(
            response_modalities=['AUDIO'], max_output_tokens=production['max_output_tokens'],
            speech_config=types.SpeechConfig(multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[types.SpeakerVoiceConfig(speaker=s,
                    voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=v))) for s, v in production['voices'].items()]))))
    candidates = response.candidates or []
    if not candidates or str(candidates[0].finish_reason).split('.')[-1] != 'STOP':
        raise ValueError('Gemini did not finish normally; usage reservation retained')
    payloads = [p.inline_data for p in candidates[0].content.parts if p.inline_data is not None]
    if len(payloads) != 1 or not isinstance(payloads[0].data, bytes):
        raise ValueError('Expected one audio response')
    pcm = normalize_audio(payloads[0].data, payloads[0].mime_type)
    usage = response.usage_metadata
    return pcm, getattr(usage, 'prompt_token_count', None), getattr(usage, 'candidates_token_count', None)


def build(script, production, sample=False, output_stem=None):
    if not sample and not production.get('voice_sample_approved'):
        raise ValueError('Full episode generation awaits explicit user voice-sample approval')
    from google import genai
    from google.genai import types
    audits = ROOT / 'publishing/spotify-jpn' / ('sample-audit' if sample else f'audits/{script.stem}')
    verify_audits(script, audits)
    plan = chunk_turns(parse_script(script), production['chunk_max_characters'])
    stem = output_stem or script.stem
    work = CACHE / stem
    work.mkdir(parents=True, exist_ok=True)
    budget = Budget(LEDGER, production)
    client, pieces, timeline, position, previous_section = None, [], [], 0.0, None
    for i, turns in enumerate(plan):
        settings = {k: production[k] for k in ('model', 'voices', 'style', 'max_output_tokens')}
        pronunciation = ROOT / 'publishing/spotify-jpn/pronunciation.json'
        settings['pronunciation_sha256'] = sha(pronunciation) if pronunciation.exists() else None
        key = hashlib.sha256(json.dumps({'turns': turns, 'settings': settings, 'spoken_version': 2},
                            sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        pcm_path, meta_path = work / f'{key}.pcm', work / f'{key}.json'
        if pcm_path.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text())
            if meta['pcm_sha256'] != sha(pcm_path):
                raise ValueError('Corrupt audio cache; preserve it for inspection')
            pcm = pcm_path.read_bytes()
            print(f'Chunk {i + 1}/{len(plan)}: cached', flush=True)
        else:
            if client is None:
                client = genai.Client(api_key=api_key(), http_options=types.HttpOptions(
                    timeout=180000, retry_options=types.HttpRetryOptions(attempts=1)))
            reservation = budget.reserve(json.dumps([turns, settings], ensure_ascii=False),
                                         production['max_output_tokens'], key)
            # No automatic retries: every new invocation reserves all potentially billed attempts.
            pcm, input_tokens, output_tokens = synthesize(client, turns, production)
            seconds = len(pcm) / (RATE * 2)
            budget.settle(reservation, input_tokens, output_tokens, seconds)
            units = sum(text_units(t['text']) for t in turns)
            if seconds < units / 1000 * 60 or seconds > units / 100 * 60 + 10:
                raise ValueError('Suspicious Japanese speech duration; inspect before retrying')
            pcm_path.write_bytes(pcm)
            atomic_json(meta_path, {'pcm_sha256': sha(pcm_path), 'request_id': reservation['id'],
                                   'duration_seconds': seconds, 'turns': turns, 'settings': settings})
            print(f'Chunk {i + 1}/{len(plan)}: {seconds:.1f} seconds; usage logged', flush=True)
        if pieces:
            gap = 1.2 if turns[0]['section'] != previous_section else .35
            silence = b'\x00' * (round(gap * RATE) * 2)
            pieces.append(silence)
            position += gap
        seconds = len(pcm) / (RATE * 2)
        timeline.append({'start_seconds': position, 'end_seconds': position + seconds,
                         'turns': turns, 'cache_key': key})
        pieces.append(pcm)
        position += seconds
        previous_section = turns[-1]['section']
    joined = work / 'assembled.wav'
    with wave.open(str(joined), 'wb') as wav:
        wav.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        wav.writeframes(b''.join(pieces))
    output = ROOT / 'mindmaps-podcast/ja/audio' / f'{stem}.mp3'
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(joined), '-c:a', 'libmp3lame',
                    '-b:a', '96k', '-metadata', f'title={script.stem} · 日本語版', str(output)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output), '-f', 'null', '-'], check=True)
    report = {'script_sha256': sha(script), 'audio_sha256': sha(output), 'duration_seconds': position,
              'timeline': timeline, 'audio': str(output.relative_to(ROOT)), 'text_audits': str(audits.relative_to(ROOT)),
              'audio_verification': 'decode_passed; speech recognition and listening pending',
              'budget_committed_usd': budget.committed, 'sample': sample, 'settings': settings}
    atomic_json(output.with_suffix('.json'), report)
    print(f'{output.relative_to(ROOT)}: {position:.1f} seconds; committed estimate ${budget.committed:.4f}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('script', type=Path)
    parser.add_argument('--sample', action='store_true')
    parser.add_argument('--comparison', action='store_true', help='Sample-only Flash-Lite comparison; never changes production settings')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        script = args.script.resolve()
        if not script.is_relative_to(ROOT / 'mindmaps-podcast/ja'):
            raise ValueError('Japanese scripts must stay inside mindmaps-podcast/ja')
        if args.sample and script != ROOT / 'mindmaps-podcast/ja/voice-sample.md':
            raise ValueError('--sample is reserved for the review excerpt, not full episodes')
        production = json.loads(PRODUCTION.read_text())
        if args.comparison:
            if not args.sample:
                raise ValueError('Comparison mode is only for the review sample')
            production = {**production, 'model': 'gemini-3.8-flash-lite-tts',
                          'pricing': {**production['pricing'], 'output_usd_per_million': 6.0}}
        if args.dry_run:
            turns = parse_script(script)
            plan = chunk_turns(turns, production['chunk_max_characters'])
            print(json.dumps({'turns': len(turns), 'characters': sum(text_units(t['text']) for t in turns),
                              'chunks': len(plan), 'voice_sample_approved': production['voice_sample_approved'],
                              'new_requests_sent': 0}, ensure_ascii=False))
        else:
            with production_lock():
                build(script, production, args.sample,
                      output_stem='voice-sample-flash-lite' if args.comparison else None)
    except Exception as exc:
        # Do not print provider exceptions, which can contain sensitive request data.
        if isinstance(exc, (ValueError, FileNotFoundError)):
            parser.exit(1, f'Stopped: {exc}\n')
        code = getattr(exc, 'code', None)
        if code == 429:
            details = json.dumps(getattr(exc, 'details', None), default=str)
            quotas = re.findall(r'"quotaId"\s*:\s*"([A-Za-z0-9_]+)"', details)
            delays = re.findall(r'"retryDelay"\s*:\s*"([0-9.s]+)"', details)
            print(f'Quota identifiers: {quotas}; retry delays: {delays}', flush=True)
        status = f' (HTTP {code})' if isinstance(code, int) else ''
        parser.exit(1, f'Stopped: {type(exc).__name__}{status}; completed caches and cost reservations retained.\n')


if __name__ == '__main__':
    main()
