"""Render Japanese transcript and glossary reading pages, without adding an audio player."""
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'mindmaps-podcast/ja'


def annotated(text, glossary, seen):
    by_term = {t['term']: t for t in glossary}
    pattern = '|'.join(re.escape(t) for t in sorted(by_term, key=len, reverse=True))
    parts, cursor = [], 0
    for match in re.finditer(pattern, text):
        parts.append(html.escape(text[cursor:match.start()]))
        term = match[0]
        item = by_term[term]
        if term in seen:
            parts.append(html.escape(term))
        else:
            seen.add(term)
            parts.append(f'<ruby>{html.escape(term)}<rp>（</rp><rt>{html.escape(item["reading"])}</rt><rp>）</rp></ruby>')
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    return ''.join(parts)


def page(title, body, depth=0):
    prefix = '../' * (depth + 2)
    home = '../' if depth else './'
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Mastering Causal Metrics (JPN)</title>
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/transcript.css?v=1">
<script src="{prefix}assets/transcript-theme.js?v=1" defer></script>
<style>body{{line-height:1.95}}rt{{font-size:.6em}}ruby{{ruby-position:over}}.glossary-term{{margin-top:1.8rem}}.english{{color:var(--muted,#9cabc5)}}.chapter-links li{{margin:.8rem 0}}.cover{{max-width:240px;width:100%;height:auto;border-radius:12px}}.passage-text{{overflow-wrap:anywhere}}a:focus-visible,button:focus-visible{{outline:3px solid #fb7185;outline-offset:4px}}</style>
</head><body><a class="skip-link" href="#transcript">本文へ移動</a>
<header class="page-header"><a href="{home}index.html">← 日本語版の案内</a>
<button type="button" id="transcript-theme" hidden aria-pressed="false">表示テーマを切り替える</button></header>
<main id="transcript"><p class="eyebrow">Mastering Causal Metrics (JPN)</p>
<h1>{html.escape(title)}</h1>{body}</main></body></html>\n'''


def main():
    config = json.loads((ROOT / 'publishing/spotify-jpn/config.json').read_text())
    state = json.loads((ROOT / 'publishing/spotify-jpn/state.json').read_text())
    glossary_data = json.loads((DEST / 'glossary.json').read_text())
    glossary = glossary_data['terms']
    transcript_directory = DEST / 'transcripts'
    transcript_directory.mkdir(parents=True, exist_ok=True)
    items = []
    for episode in config['episodes']:
        source = transcript_directory / (episode['id'] + '.json')
        if not source.exists():
            continue
        data = json.loads(source.read_text())
        if data.get('unreviewed_flagged_spans', 0) and not data.get('flag_review_complete'):
            raise ValueError(f'Review speech discrepancies before publishing {episode["id"]}')
        if data.get('unreviewed_number_flags', 0) and not data.get('number_review_complete'):
            raise ValueError(f'Review numeric speech discrepancies before publishing {episode["id"]}')
        seen, passages = set(), []
        sections = {s['segment']: (i, s) for i, s in enumerate(data['sections'])}
        contents = ''.join(f'<li><a href="#section-{i}">{html.escape(s["title"])}</a></li>'
                           for i, s in enumerate(data['sections']))
        for i, segment in enumerate(data['segments']):
            if i in sections:
                n, section = sections[i]
                passages.append(f'<h2 id="section-{n}">{html.escape(section["title"])}</h2>')
            label = '司会' if segment['speaker'] == 'HOST' else '先生'
            seconds = int(segment['start'])
            passages.append(f'<div class="passage"><p class="speaker">{label} '
                            f'<span class="timestamp">{seconds // 60:02}:{seconds % 60:02}</span></p>'
                            f'<p class="passage-text">{annotated(segment["text"],glossary,seen)}</p></div>')
        remote = state.get('episodes', {}).get(episode['id'], {}).get('public_url')
        spotify = f'<p><a href="{html.escape(remote,quote=True)}">Spotifyで聴く</a></p>' if remote else ''
        spelling_note = html.escape(data.get('english_term_spelling_note', ''))
        # chapters with a language lesson (built by the local write-japanese-lesson skill) link to it
        has_lesson = (DEST / 'study' / (episode['id'] + '.html')).exists()
        lesson = f' · <a href="../study/{episode["id"]}.html">日本語レッスン（N2→N1）</a>' if has_lesson else ''
        body = ('<p class="note">独立した学習補助番組のオリジナル原稿に基づくAI音声です。'
                '音声認識を使って原稿と照合しています。表示時刻は近似です。' + spelling_note + '</p>' + spotify +
                f'<p><a href="{episode["id"]}.txt">日本語テキストを開く</a> · '
                '<a href="../glossary.html">専門用語の日英対訳・読み方</a>' + lesson + '</p>' +
                f'<nav aria-label="この章の目次"><ul>{contents}</ul></nav><article aria-label="文字起こし">' +
                '\n'.join(passages) + '</article>')
        source.with_suffix('.html').write_text(page(episode['title'], body, depth=1))
        lesson_item = f' · <a href="study/{episode["id"]}.html">日本語レッスン（N2→N1）</a>' if has_lesson else ''
        items.append(f'<li><a href="transcripts/{episode["id"]}.html">{html.escape(episode["title"])}</a>{lesson_item}</li>')
    glossary_body = ['<p>専門用語の読み方、英語表現、やさしい日本語での説明です。</p>']
    for term in glossary:
        glossary_body.append(f'<section class="glossary-term"><h2>{html.escape(term["term"])}</h2>'
                             f'<p>{html.escape(term["reading"])}</p><p class="english">{html.escape(term["english"])}</p>'
                             f'<p>{html.escape(term["explanation"])}</p></section>')
    (DEST / 'glossary.html').write_text(page('専門用語の日英対訳・読み方', ''.join(glossary_body)))
    show_url = state.get('show', {}).get('public_url')
    show_link = f'<p><a href="{html.escape(show_url,quote=True)}">Spotifyで番組を聴く</a></p>' if show_url else ''
    body = ('<p><a href="../../podcasts-ja.html">日本語の音声とマインドマップを開く →</a></p>' + show_link + '<p>学生と先生の対話で、因果推論を日本語で学ぶ全6章の番組です。日本語を学習中の方にも、'
            '専門用語の読み方と日英対訳をご用意しています。</p>'
            '<p><a href="glossary.html">専門用語の日英対訳・読み方</a></p>'
            '<nav aria-label="公開済みの章"><ul class="chapter-links">' + ''.join(items) + '</ul></nav>'
            '<p class="note">制作：Carlos Mendez。AngristとPischkeによるMastering ’Metrics（2015年）を学ぶための'
            '独立した補助教材であり、公式のオーディオブックではありません。AI音声を使用しています。</p>'
            '<p><a href="../../index.html">英語版の学習サイトへ</a></p>')
    (DEST / 'index.html').write_text(page('因果推論を日本語で学ぶ', body))
    print(f'Rendered {len(items)} Japanese transcript pages, glossary and index')


if __name__ == '__main__':
    main()
