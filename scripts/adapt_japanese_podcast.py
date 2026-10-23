"""Faithfully adapt existing original English podcast dialogue, retaining turn-level provenance."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from japanese_podcast_audio import ROOT, PRODUCTION, LEDGER, Budget, atomic_json, api_key, production_lock, parse_script

TEXT_MODEL = 'gemini-3.8-flash'
HEADINGS = {'Opening': 'オープニング', 'Part 1: The Question': '第1部：問い',
            'Part 2: The Investigation': '第2部：検証', 'Part 3: The Resolution': '第3部：結論',
            'Wrap-up': 'まとめ'}


def source_turns(path):
    result, section = [], ''
    for line in path.read_text().splitlines():
        if line.startswith('## '):
            section = line[3:]
        match = re.fullmatch(r'(HOST|ECONOMIST): (.+)', line)
        if match:
            result.append({'id': len(result) + 1, 'speaker': match[1], 'text': match[2], 'section': section})
    if not result or any(t['section'] not in HEADINGS for t in result):
        raise ValueError('Unexpected English script structure')
    return result


def validate_translation(source, translated):
    if len(source) != len(translated):
        raise ValueError('Translation omitted or added turns')
    for old, new in zip(source, translated):
        if new.get('id') != old['id'] or not isinstance(new.get('text'), str) or not new['text'].strip():
            raise ValueError('Translation turn identity/format mismatch')
        if '\n' in new['text'] or not re.search(r'[ぁ-んァ-ヶ一-龯]', new['text']):
            raise ValueError('Translation must be Japanese single-line spoken turns')
        numeric = r'\d+(?:,\d{3})*(?:\.\d+)?'
        expected = Counter(re.findall(numeric, old['text']))
        # Japanese has no word boundaries around digits.
        actual = Counter(re.findall(numeric, new['text']))
        missing = expected - actual
        if missing:
            raise ValueError(f'Turn {old["id"]}: missing source numerals {dict(missing)}')


def adapt(number):
    from google import genai
    from google.genai import types
    production = json.loads(PRODUCTION.read_text())
    if not production['voice_sample_approved']:
        raise ValueError('Voice sample is not approved')
    config = json.loads((ROOT / 'publishing/spotify-jpn/config.json').read_text())
    episode = next(e for e in config['episodes'] if e['number'] == number)
    source = ROOT / 'mindmaps-podcast' / (episode['id'] + '.md')
    output = ROOT / 'mindmaps-podcast/ja' / source.name
    provenance = ROOT / 'publishing/spotify-jpn/adaptations' / (episode['id'] + '.json')
    if output.exists():
        print(f'{output.relative_to(ROOT)} already exists; preserve it for review')
        return
    turns = source_turns(source)
    glossary = json.loads((ROOT / 'mindmaps-podcast/ja/glossary.json').read_text())['terms']
    prompt = (
        'You are translating an original, reviewed educational podcast into natural polite Japanese for '
        'econometrics beginners and Japanese learners around JLPT N2. Produce a FAITHFUL FULL ADAPTATION, '
        'not a summary. Translate EVERY turn completely, including every example, assumption, limitation, '
        'numerical finding, prediction, worked calculation, recap and application question. Preserve the '
        'meaning, speaker roles, order and ALL source Arabic numerals exactly (including comma grouping and '
        'decimal trailing zeroes). Do not introduce unsupported findings or localize American research into '
        'Japanese research. Keep the student/teacher conversational teaching style, shorter clear Japanese '
        'sentences, and define technical terms naturally. Retain all substantive coverage even if long. '
        'Use the supplied terminology glossary consistently; include English technical equivalents on first '
        'introduction only if useful, not repeated on every turn. Reading aids will be added separately: '
        'DO NOT include parenthetic kana readings, furigana, markdown, stage directions or pronunciation tags. '
        'Write normal Japanese spoken text, with パーセント and パーセントポイント distinguished correctly. '
        'Do not include English speaker names in text. Do not read Python syntax or URLs. Translate the pause '
        'invitation as 音声を一度止めて考えてみてください. The approved edition has a warm male HOST '
        'and a calm female ECONOMIST. No need to introduce their names. Reply ONLY valid JSON with shape '
        '{"turns":[{"id":1,"text":"Japanese translation"},...]}; one result per source turn. '
        'The content is our original companion script, not text from the original book.\nTerminology:\n' +
        json.dumps(glossary, ensure_ascii=False) + '\nSource turns:\n' + json.dumps(turns, ensure_ascii=False))
    work = ROOT / '.work/podcast-ja/adaptation' / episode['id']
    work.mkdir(parents=True, exist_ok=True)
    (work / 'prompt.txt').write_text(prompt)
    text_production = {**production, 'model': TEXT_MODEL, 'pricing': {
        'checked_at': '2026-10-23', 'valid_through': '2026-12-31',
        'input_usd_per_million': .75, 'output_usd_per_million': 3.75,
        'audio_tokens_per_second': 0, 'source': 'https://ai.google.dev/gemini-api/docs/pricing'}}
    response_path = work / 'response.json'
    if response_path.exists():
        translated = json.loads(response_path.read_text())['turns']
    else:
        client = genai.Client(api_key=api_key(), http_options=types.HttpOptions(
            timeout=300000, retry_options=types.HttpRetryOptions(attempts=1)))
        budget = Budget(LEDGER, text_production)
        reservation = budget.reserve(prompt, 32768, hashlib.sha256(prompt.encode()).hexdigest())
        response = client.models.generate_content(model=TEXT_MODEL, contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=32768, response_mime_type='application/json',
                temperature=.2, thinking_config=types.ThinkingConfig(thinking_budget=0)))
        usage = response.usage_metadata
        output_tokens = (getattr(usage, 'candidates_token_count', 0) or 0) + (getattr(usage, 'thoughts_token_count', 0) or 0)
        budget.settle(reservation, getattr(usage, 'prompt_token_count', None), output_tokens, 0)
        if not response.candidates or str(response.candidates[0].finish_reason).split('.')[-1] != 'STOP':
            raise ValueError('Translation response truncated; no script written')
        response_path.write_text(response.text)
        translated = json.loads(response.text)['turns']
    validate_translation(turns, translated)
    lines = ['# ' + episode['title'], '',
             'Two voices: HOST, a curious student, and ECONOMIST, a friendly econometrics teacher.', '']
    last_section = None
    for old, new in zip(turns, translated):
        if old['section'] != last_section:
            lines.extend(['## ' + HEADINGS[old['section']], ''])
        lines.extend([old['speaker'] + ': ' + new['text'].strip(), ''])
        last_section = old['section']
    output.write_text('\n'.join(lines))
    parse_script(output)
    atomic_json(provenance, {'source': str(source.relative_to(ROOT)),
                'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'script_sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'model': TEXT_MODEL,
                'created_at': datetime.now(timezone.utc).isoformat(), 'review_status': 'awaiting_independent_audit',
                'turn_count': len(turns), 'turns': [{'id': old['id'], 'speaker': old['speaker'],
                    'section': HEADINGS[old['section']], 'english': old['text'], 'japanese': new['text']}
                    for old, new in zip(turns, translated)]})
    print(f'{output.relative_to(ROOT)}: {len(turns)} source-matched turns; ready for independent review', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapter', type=int, choices=range(1, 7))
    args = parser.parse_args()
    try:
        with production_lock('adaptation'):
            adapt(args.chapter)
    except Exception as exc:
        if isinstance(exc, (ValueError, FileNotFoundError)):
            parser.exit(1, f'Stopped: {exc}\n')
        code = getattr(exc, 'code', None)
        parser.exit(1, f'Stopped: {type(exc).__name__}; HTTP {code}; ledger retained.\n')
