"""Create web Opus recordings from the local lossless podcast masters.

Run from the repository root. Original MP3s remain browser fallbacks. No API calls.
"""
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=codec_name,channels', '-of', 'json', str(path)
    ], text=True))


def compress(transcript):
    stem = transcript.stem
    master = Path('.work/podcast') / stem / 'episode.wav'
    mp3 = Path('mindmaps-podcast/audio') / (stem + '.mp3')
    output = mp3.with_suffix('.opus')
    temporary = output.with_suffix('.tmp.opus')
    episode = json.loads(transcript.read_text())
    if hashlib.sha256(mp3.read_bytes()).hexdigest() != episode['audio_sha256']:
        raise ValueError(f'{stem}: MP3 does not match the aligned transcript')
    master_duration = float(probe(master)['format']['duration'])
    if abs(master_duration - episode['duration']) > .15:
        raise ValueError(f'{stem}: lossless master does not match transcript timing')
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(master),
        '-map_metadata', '-1', '-vn', '-ac', '1', '-c:a', 'libopus', '-b:a', '48k',
        '-vbr', 'on', '-application', 'audio', '-compression_level', '10', str(temporary)
    ], check=True)
    info = probe(temporary)
    duration = float(info['format']['duration'])
    assert info['streams'][0]['codec_name'] == 'opus'
    assert info['streams'][0]['channels'] == 1
    if abs(duration - master_duration) > .05:
        raise ValueError(f'{stem}: compressed duration changed')
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror',
        '-i', str(temporary), '-f', 'null', '-'
    ], check=True)
    temporary.replace(output)
    episode['audio_variants'] = {
        'opus': {
            'path': str(output), 'codec': 'opus', 'target_bitrate_kbps': 48,
            'duration': round(duration, 3), 'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest()
        },
        'mp3': {'path': str(mp3), 'sha256': episode['audio_sha256']}
    }
    transcript.write_text(json.dumps(episode, ensure_ascii=False, indent=2) + '\n')
    before, after = mp3.stat().st_size, output.stat().st_size
    print(f'{stem}: {before / 1e6:.1f} → {after / 1e6:.1f} MB '
          f'({1 - after / before:.1%} smaller); decode and timing PASS', flush=True)
    return before, after


if __name__ == '__main__':
    transcripts = sorted(Path('mindmaps-podcast/transcripts').glob('ch0*.json'))
    if len(transcripts) != 6:
        raise ValueError('Expected the six completed chapter transcripts')
    with ThreadPoolExecutor(max_workers=2) as pool:
        sizes = list(pool.map(compress, transcripts))
    before, after = (sum(s[index] for s in sizes) for index in (0, 1))
    print(f'Total: {before / 1e6:.1f} → {after / 1e6:.1f} MB '
          f'({1 - after / before:.1%} smaller)', flush=True)
