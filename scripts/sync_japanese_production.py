"""Refresh local preparation evidence without inventing or replacing Spotify observations."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from japanese_podcast_audio import ROOT, atomic_json, sha, parse_script, verify_audits


def main():
    folder = ROOT / 'publishing/spotify-jpn'
    config = json.loads((folder/'config.json').read_text())
    state = json.loads((folder/'state.json').read_text())
    for episode in config['episodes']:
        stem = episode['id']
        script = ROOT / 'mindmaps-podcast/ja' / f'{stem}.md'
        local = {'script':'missing','audio':'missing','transcript':'missing'}
        if script.exists():
            turns = parse_script(script)
            local.update(script='adapted',script_sha256=sha(script),turn_count=len(turns))
            provenance_path = folder/'adaptations'/f'{stem}.json'
            if provenance_path.exists():
                provenance=json.loads(provenance_path.read_text())
                if len(provenance['turns']) != len(turns):
                    raise ValueError(f'{stem}: manually reconcile changed turn structure')
                provenance.setdefault('initial_translation_sha256',provenance['script_sha256'])
                provenance['script_sha256']=sha(script)
                for before,now in zip(provenance['turns'],turns):
                    before['japanese']=now['text']
                    before['section']=now['section']
                try:
                    verify_audits(script,folder/'audits'/stem)
                    local['script']='reviewed'
                    provenance['review_status']='independent_audits_pass'
                except (ValueError,FileNotFoundError):
                    provenance['review_status']='awaiting_current_independent_audit'
                atomic_json(provenance_path,provenance)
        audio=ROOT/episode['audio']
        if audio.exists() and audio.with_suffix('.json').exists():
            report=json.loads(audio.with_suffix('.json').read_text())
            if sha(audio) != report['audio_sha256']:
                raise ValueError(f'{stem}: changed audio after synthesis')
            local.update(audio='generated_decode_passed',audio_sha256=sha(audio),duration_seconds=report['duration_seconds'])
        elif audio.exists():
            local['audio']='encoding_or_verification_in_progress'
        transcript=ROOT/'mindmaps-podcast/ja/transcripts'/f'{stem}.json'
        if transcript.exists():
            data=json.loads(transcript.read_text())
            if data['audio_sha256'] != local.get('audio_sha256'):
                raise ValueError(f'{stem}: stale transcript')
            needs_review = (data.get('unreviewed_flagged_spans', 0) and not data.get('flag_review_complete')) or (data.get('unreviewed_number_flags', 0) and not data.get('number_review_complete'))
            local.update(transcript='requires_review' if needs_review else 'aligned',
                         unreviewed_flagged_spans=data['unreviewed_flagged_spans'],
                         unreviewed_number_flags=data.get('unreviewed_number_flags',0))
            episode.update(transcript=str(transcript.with_suffix('.vtt').relative_to(ROOT)),
                transcript_text=str(transcript.with_suffix('.txt').relative_to(ROOT)),
                alignment=str(transcript.relative_to(ROOT)),
                transcript_url=f'https://cmg777.github.io/intro2causal/mindmaps-podcast/ja/transcripts/{stem}.txt')
            if '文字起こし：' not in episode['description']:
                episode['description'] += (f'\n\n文字起こし：https://cmg777.github.io/intro2causal/mindmaps-podcast/ja/transcripts/{stem}.html'
                    '\n用語集：https://cmg777.github.io/intro2causal/mindmaps-podcast/ja/glossary.html\n文字起こしの時刻は近似です。')
        episode['production_status']=local['transcript'] if transcript.exists() else local['audio'] if audio.exists() else local['script']
        record=state['episodes'].setdefault(stem,{'status':'not_uploaded','remote_id':None})
        record['local_preparation']=local
    atomic_json(folder/'config.json',config)
    atomic_json(folder/'state.json',state)
    print('Updated Japanese local preparation evidence; preserved remote observations')


if __name__=='__main__':
    main()
