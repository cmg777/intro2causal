"""Render the published transcript JSON as standalone, JavaScript-free reading pages."""
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def render(episode, number):
    title = f"Chapter {number}: {episode['title']}"
    sections = {section['segment']: (index, section['title'])
                for index, section in enumerate(episode['sections'])}
    contents = '\n'.join(
        f'<li><a href="#section-{index}">{html.escape(section["title"])}</a></li>'
        for index, section in enumerate(episode['sections']))
    passages = []
    for index, segment in enumerate(episode['segments']):
        if index in sections:
            section_index, heading = sections[index]
            passages.append(f'<h2 id="section-{section_index}">{html.escape(heading)}</h2>')
        seconds = int(segment['start'])
        timestamp = f'{seconds // 60:02}:{seconds % 60:02}'
        passages.append(
            f'<div class="passage"><p class="speaker">{html.escape(segment["speaker"])} '
            f'<span class="timestamp">{timestamp}</span></p>'
            f'<p class="passage-text">{html.escape(segment["text"])}</p></div>')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — Transcript | Mastering Causal Metrics</title>
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../assets/transcript.css?v=1">
  <script src="../../assets/transcript-theme.js?v=1" defer></script>
</head>
<body>
  <a class="skip-link" href="#transcript">Skip to transcript</a>
  <header class="page-header">
    <a href="../../index.html#chapter-{number}">← Back to Chapter {number}</a>
    <button type="button" id="transcript-theme" hidden aria-pressed="false">Light theme</button>
  </header>
  <main id="transcript">
    <p class="eyebrow">Mastering Causal Metrics · Podcast transcript</p>
    <h1>{html.escape(title)}</h1>
    <p class="note">AI-generated narration from an original educational script. Transcript timing is approximate.</p>
    <nav aria-label="Transcript sections"><ul>{contents}</ul></nav>
    <article aria-label="Full transcript">
{chr(10).join(passages)}
    </article>
  </main>
</body>
</html>
'''


def main():
    for source in sorted((ROOT / 'mindmaps-podcast/transcripts').glob('ch[0-9][0-9]-*.json')):
        episode = json.loads(source.read_text(encoding='utf-8'))
        source.with_suffix('.html').write_text(render(episode, int(source.stem[2:4])), encoding='utf-8')
        print(f'Rendered {source.stem}')


if __name__ == '__main__':
    main()
