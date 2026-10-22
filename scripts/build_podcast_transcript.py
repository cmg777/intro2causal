"""Align a podcast script to offline whisper.cpp recognition, using the TTS chunk cache.

No API calls or model generation occur here. See mindmaps-podcast/transcripts/README.md.
"""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
from pathlib import Path


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower().replace("’", "'"))


def plan_chunks(script):
    # Match the audio assembler's section/turn boundaries and 380-word chunk target.
    sections = []
    for line in script.splitlines():
        if line.startswith('## '):
            sections.append({'title': line[3:].strip(), 'turns': []})
        match = re.match(r'(HOST|ECONOMIST): (.+)', line)
        if match and sections:
            sections[-1]['turns'].append({'speaker': match[1].title(), 'text': match[2]})
    count_words = lambda text: len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.,-]*", text))
    chunks = []
    for section in sections:
        total = sum(count_words(t['text']) for t in section['turns'])
        target = total / max(1, -(-total // 380))
        turns, count = [], 0
        for index, turn in enumerate(section['turns']):
            turns.append(turn)
            count += count_words(turn['text'])
            pause = bool(re.search(r'\bpause the episode\b', turn['text'], re.I))
            if pause or (count >= target and index < len(section['turns']) - 1):
                chunks.append({'title': section['title'], 'turns': turns, 'pause': pause})
                turns, count = [], 0
        if turns:
            chunks.append({'title': section['title'], 'turns': turns, 'pause': False})
    return chunks


def stamp(seconds, vtt=False):
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, ms = divmod(ms, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02}.{ms:03}' if vtt else f'{hours * 60 + minutes:02}:{seconds:02}'


def build(args):
    recognition = json.loads(args.recognition.read_text())['transcription']
    heard = []
    for segment in recognition:
        tokens = words(segment['text'])
        start, end = segment['offsets']['from'] / 1000, segment['offsets']['to'] / 1000
        for index, token in enumerate(tokens):
            heard.append((token, start + (end - start) * index / len(tokens)))
    chunks = plan_chunks(args.script.read_text())
    sections, segments, report = [], [], []
    offset, previous = 0., None
    for i, chunk in enumerate(chunks, 1):
        files = list(args.cache.glob(f'{i:02}-*.pcm'))
        if len(files) != 1:
            raise ValueError(f'Expected exactly one cached PCM file for chunk {i}')
        if previous is not None:
            offset += 1.2 if previous != chunk['title'] else .35
        if previous != chunk['title']:
            title = re.sub(r'^Part \d+: ', '', chunk['title'])
            sections.append({'title': title, 'start': round(offset, 3), 'segment': len(segments)})
        length = files[0].stat().st_size / 48000  # 24 kHz, mono, 16-bit PCM.
        chunk_words, turn_starts = [], []
        for turn in chunk['turns']:
            turn_starts.append(len(chunk_words))
            chunk_words.extend(words(turn['text']))
        local = [(word, time) for word, time in heard if offset <= time < offset + length]
        matcher = difflib.SequenceMatcher(None, chunk_words, [word for word, _ in local], autojunk=False)
        anchors = {}
        for block in matcher.get_matching_blocks():
            for j in range(block.size):
                anchors[block.a + j] = local[block.b + j][1]
        coverage = len(anchors) / len(chunk_words)
        if coverage < .75:
            raise ValueError(f'Chunk {i}: only {coverage:.1%} matched; inspect recognition before publishing')
        report.append({'chunk': i, 'matched': round(coverage, 4)})
        for j, turn in enumerate(chunk['turns']):
            begin = turn_starts[j]
            finish = turn_starts[j + 1] if j + 1 < len(turn_starts) else len(chunk_words)
            matches = [key for key in anchors if begin <= key < finish]
            if len(matches) / (finish - begin) < .5:
                raise ValueError(f'Chunk {i}, turn {j + 1}: insufficient alignment')
            # Locate paragraph onset with nearby recognized words. Missing initial words
            # are interpolated between anchors; estimates stay inside the actual chunk.
            left = max((key for key in anchors if key <= begin), default=-1)
            right = min((key for key in anchors if key >= begin), default=len(chunk_words))
            left_time = anchors.get(left, offset)
            right_time = anchors.get(right, offset + length)
            start = left_time if left == right else left_time + (right_time - left_time) * (begin - left) / (right - left)
            if j == 0:
                start = offset
            segments.append({'start': round(start, 3), 'end': round(offset + length, 3),
                             'speaker': turn['speaker'], 'text': turn['text']})
            if j > 0:
                segments[-2]['end'] = round(start, 3)
        offset += length + (4 if chunk['pause'] else 0)
        previous = chunk['title']
    measured = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                     'format=duration', '-of', 'default=nw=1:nk=1', str(args.audio)], text=True))
    if abs(measured - offset) > .15:
        raise ValueError('Cached chunks do not match the recording duration')
    for index, segment in enumerate(segments):
        assert segment['start'] < segment['end']
        if index:
            assert segment['start'] >= segments[index - 1]['end']
    title = args.script.read_text().splitlines()[0].removeprefix('# ').split(': a podcast')[0]
    output = {'title': title, 'duration': round(measured, 3),
              'timing': 'Script paragraphs aligned to local Whisper recognition; section boundaries from source audio chunks.',
              'audio_sha256': hashlib.sha256(args.audio.read_bytes()).hexdigest(),
              'sections': sections, 'segments': segments, 'alignment': report}
    args.output.mkdir(parents=True, exist_ok=True)
    stem = args.output / args.script.stem
    stem.with_suffix('.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    text, vtt = [output['title'], ''], ['WEBVTT', '']
    for index, segment in enumerate(segments):
        for section in sections:
            if section['segment'] == index:
                text.extend([section['title'], ''])
        text.extend([f"[{stamp(segment['start'])}] {segment['speaker']}: {segment['text']}", ''])
        vtt.extend([str(index + 1), f"{stamp(segment['start'], True)} --> {stamp(segment['end'], True)}",
                    f"<v {segment['speaker']}>{segment['text']}", ''])
    stem.with_suffix('.txt').write_text('\n'.join(text))
    stem.with_suffix('.vtt').write_text('\n'.join(vtt))
    print(f'{len(sections)} sections, {len(segments)} paragraphs; minimum chunk match {min(r["matched"] for r in report):.1%}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recognition', type=Path, required=True)
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--audio', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('mindmaps-podcast/transcripts'))
    build(parser.parse_args())
