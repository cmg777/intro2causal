"""Validate podcast assets and prepare a manifest; never calls Spotify or publishes."""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


def sha256(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def seconds(stamp):
    h, m, s = stamp.split(':')
    if not (0 <= int(m) < 60 and 0 <= float(s) < 60):
        raise ValueError(f'Invalid timestamp: {stamp}')
    return int(h) * 3600 + int(m) * 60 + float(s)


def validate_vtt(path, duration):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('WEBVTT') or path.stat().st_size > 5_000_000:
        raise ValueError(f'Invalid VTT header or size: {path}')
    previous, count = 0., 0
    for block in re.split(r'\n\s*\n', text.strip()):
        if '-->' not in block:
            continue
        match = re.search(r'^(\d{2,}:\d{2}:\d{2}\.\d{3}) --> (\d{2,}:\d{2}:\d{2}\.\d{3})$', block, re.M)
        if not match:
            raise ValueError(f'Invalid cue: {path}')
        start, end = map(seconds, match.groups())
        if not previous <= start < end <= duration + .2:
            raise ValueError(f'Nonmonotonic or out-of-range cue: {path}')
        if not block[match.end():].strip():
            raise ValueError(f'Empty cue: {path}')
        previous, count = end, count + 1
    if not count or abs(duration - previous) > 2:
        raise ValueError(f'Empty or truncated transcript: {path}')
    return count


def check_url(url):
    if not url.startswith('https://'):
        raise ValueError(f'Public URL must use HTTPS: {url}')
    with urlopen(Request(url, headers={'User-Agent': 'PodcastAssetCheck/1.0'}), timeout=30) as response:
        body = response.read()
        if response.status != 200 or not body:
            raise ValueError(f'Unavailable public link: {url}')
        return body


def validate_artwork(artwork):
    from PIL import Image
    with Image.open(artwork) as picture:
        width, height = picture.size
        if width != height or not 1400 <= width <= 3000 or picture.mode != 'RGB':
            raise ValueError('Artwork must be square RGB, 1400–3000 pixels')


def prepare(config_path, state_path, check_links=False):
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text())
    root = (config_path.parent / config.get('root', '../..')).resolve()
    state = json.loads(state_path.read_text()) if state_path.exists() else {
        'project_id': config['project_id'], 'show_id': None, 'episodes': {}}
    if state['project_id'] != config['project_id']:
        raise ValueError('State belongs to a different project')
    if config['schema_version'] != 1:
        raise ValueError('Unsupported configuration version')
    show = config['show']
    if not show['title'] or not show['creator'] or len(show['description']) > 600:
        raise ValueError('Missing show identity or description exceeds 600 characters')
    artwork = root / show['artwork']
    validate_artwork(artwork)
    result = {'schema_version': 1, 'project_id': config['project_id'],
              'prepared_at': datetime.now(timezone.utc).isoformat(),
              'show': dict(show, artwork=str(artwork), spotify_id=state.get('show_id')),
              'links_checked': check_links, 'episodes': []}
    if check_links:
        check_url(show['website'])
    ids, numbers = set(), set()
    for episode in config['episodes']:
        key, number = episode['id'], episode['number']
        if key in ids or number in numbers:
            raise ValueError('Duplicate episode identifier or number')
        ids.add(key)
        numbers.add(number)
        audio, transcript, alignment = (root / episode[k] for k in ('audio', 'transcript', 'alignment'))
        metadata = json.loads(alignment.read_text())
        audio_hash = sha256(audio)
        if audio_hash != metadata['audio_sha256']:
            raise ValueError(f'Audio does not match transcript alignment: {key}')
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format',
                           '-show_streams', '-of', 'json', str(audio)], text=True))
        duration = float(probe['format']['duration'])
        streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
        if audio.suffix.lower() != '.mp3' or not streams or streams[0]['channels'] not in (1, 2):
            raise ValueError(f'Expected mono or stereo MP3: {key}')
        if abs(duration - metadata['duration']) > .2:
            raise ValueError(f'Audio duration differs from alignment: {key}')
        # Decode the entire file to detect damaged or truncated audio packets.
        subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(audio),
                        '-map', '0:a:0', '-f', 'null', '-'], check=True)
        cues = validate_vtt(transcript, duration)
        if check_links:
            public_text = check_url(episode['transcript_url']).decode('utf-8')
            if public_text != transcript.with_suffix('.txt').read_text():
                raise ValueError(f'Public transcript differs from local copy: {key}')
        hashes = {'audio_sha256': audio_hash, 'transcript_sha256': sha256(transcript)}
        saved = state.get('episodes', {}).get(key, {})
        status = saved.get('status', 'not_uploaded')
        if status == 'published' and any(saved.get(k) != v for k, v in hashes.items()):
            raise ValueError(f'Published assets changed; review before replacing: {key}')
        episode_art = {}
        artwork_changed = False
        if episode.get('artwork'):
            art_path = root / episode['artwork']
            validate_artwork(art_path)
            art_hash = sha256(art_path)
            episode_art = {'artwork': str(art_path), 'artwork_sha256': art_hash}
            artwork_changed = saved.get('artwork_sha256') != art_hash
        result['episodes'].append(dict(episode, audio=str(audio), transcript=str(transcript),
            duration=duration, cues=cues, **hashes, **episode_art, status=status,
            action=('inspect_artwork_update' if artwork_changed else 'skip_published')
                if status == 'published' else 'inspect_spotify_before_upload',
            spotify=saved))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('publishing/spotify/project.json'))
    parser.add_argument('--state', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-links', action='store_true')
    args = parser.parse_args()
    state = args.state or args.config.parent / 'state.json'
    output = args.output or args.config.parent / 'manifest.json'
    result = prepare(args.config, state, args.check_links)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for episode in result['episodes']:
        print(f"{episode['id']}: {episode['duration']/60:.1f} min, {episode['cues']} cues, {episode['action']}")
    print(f'Manifest: {output}')


if __name__ == '__main__':
    main()
