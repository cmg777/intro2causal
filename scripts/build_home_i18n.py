"""Build the Spanish and Japanese home pages from index.html and i18n/home/translations.json.

Run with: uv run python scripts/build_home_i18n.py
Use --check to verify index-es.html and index-ja.html are current without writing changes.

index.html is the single source. Every translation key must match the English page,
so an edit to the English copy that is not mirrored in the translations fails loudly.
After translating, any visible English segment left on a page (outside the allowlist)
is also reported as an error.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'index.html'
TRANSLATIONS = ROOT / 'i18n/home/translations.json'
LANGS = ('es', 'ja')
SITE = 'https://cmg777.github.io/intro2causal/'
TEXT_ATTRS = ('aria-label', 'alt', 'title', 'placeholder')


def expand_chapters(data, lang):
    """Turn per-chapter templates into ordinary (english, translated) pairs."""
    pairs = []
    for chapter in data['chapters']:
        values = {'n': chapter['n'], 'slug': chapter['slug'], 'name': chapter['en'],
                  'name_xx': chapter[lang], 'open_the': '' if chapter['en'].startswith('The ') else 'the ',
                  **chapter.get(lang + '_fields', {}), **{'en_' + k: v for k, v in chapter.get('en_fields', {}).items()}}
        for template in data['chapter_templates']:
            if lang not in template:
                continue
            english = template['en'].format(**values)
            translated = template[lang].format(**values)
            pairs.append((english, translated))
    return pairs


def apply_pairs(document, pairs, lang):
    """Replace every key in one pass (longest key first) and require each to match fully."""
    table = {}
    for english, translated in pairs:
        if english in table and table[english] != translated:
            raise SystemExit(f'[{lang}] conflicting translations for {english!r}')
        table[english] = translated
    keys = sorted(table, key=len, reverse=True)
    pattern = re.compile('|'.join(re.escape(key) for key in keys))
    counts = dict.fromkeys(keys, 0)

    def replace(match):
        counts[match.group(0)] += 1
        return table[match.group(0)]

    result = pattern.sub(replace, document)
    errors = [f'[{lang}] key matched {counts[k]} of {document.count(k)} occurrences: {k[:90]!r}'
              for k in keys if counts[k] == 0]
    if errors:
        raise SystemExit('\n'.join(errors))
    return result


def apply_patterns(document, patterns, lang):
    for item in patterns:
        if lang not in item:
            continue
        document, count = re.subn(item['re'], item[lang], document)
        if count == 0:
            raise SystemExit(f'[{lang}] pattern matched nothing: {item["re"]!r}')
    return document


def localize_shell(document, lang, output):
    """Language attribute, current pill, canonical URL; drop the English-only redirect."""
    document, count = re.subn(r'  <script id="lang-redirect">.*?</script>\n', '', document, flags=re.S)
    assert count == 1, 'redirect script not found'
    document = document.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    document = document.replace(f'<link rel="canonical" href="{SITE}index.html">',
                                f'<link rel="canonical" href="{SITE}{output}">', 1)
    document = document.replace(' data-lang="en" aria-current="true"', ' data-lang="en"')
    document = document.replace(f' data-lang="{lang}"', f' data-lang="{lang}" aria-current="true"')
    return document


class Segments(HTMLParser):
    """Collect visible text and accessible-name attributes, skipping script and style."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.found = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        attrs = dict(attrs)
        for name in TEXT_ATTRS:
            if attrs.get(name):
                self.found.append(attrs[name])
        if tag == 'meta' and attrs.get('name') == 'description':
            self.found.append(attrs.get('content', ''))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.found.append(data)


def segments(document):
    parser = Segments()
    parser.feed(document)
    cleaned = (' '.join(text.split()) for text in parser.found)
    found = {text for text in cleaned if re.search(r'[A-Za-z]{3,}', text)}
    # Script copy that reaches the page: resource labels, descriptions and video credits.
    for match in re.finditer(r"(?:label|action|description):\s*(['\"])(.*?)(?<!\\)\1", document):
        found.add(match.group(2))
    found.update(re.findall(r"credit\.innerHTML = '([^']*)'", document))
    return found


def plain(text):
    return ' '.join(re.sub(r'<[^>]+>', ' ', text.replace('&amp;', '&').replace('&middot;', '·')).split())


def leftover_english(english, translated, allow):
    """English segments, or English phrases inside longer strings, that survive translation."""
    allowed = [re.compile(item) for item in allow]
    found = segments(translated)
    leftovers = segments(english) & found
    page = '\n'.join(plain(text) for text in found)
    for text in segments(english):
        for phrase in re.split(r'\s*[·—]\s*|(?<=[.?!])\s+', plain(text)):
            if len(re.findall(r'[A-Za-z]+', phrase)) >= 3 and phrase in page:
                leftovers.add(phrase)
    return sorted(text for text in leftovers if not any(rule.fullmatch(text) for rule in allowed))


def build(lang, data, english):
    config = data['languages'][lang]
    pairs = [(item['en'], item[lang]) for item in data['strings'] if lang in item]
    pairs += expand_chapters(data, lang)
    document = localize_shell(english, lang, config['output'])
    document = apply_pairs(document, pairs, lang)
    document = apply_patterns(document, data['patterns'], lang)
    leftovers = leftover_english(english, document, data['allow_english'] + config.get('allow_english', []))
    if leftovers:
        raise SystemExit(f'[{lang}] untranslated English segments:\n' + '\n'.join(f'  {t[:110]!r}' for t in leftovers))
    return ROOT / config['output'], document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='fail if generated pages are out of date')
    args = parser.parse_args()
    english = SOURCE.read_text()
    data = json.loads(TRANSLATIONS.read_text())
    stale = []
    for lang in LANGS:
        path, document = build(lang, data, english)
        if args.check:
            if not path.exists() or path.read_text() != document:
                stale.append(path.name)
        else:
            path.write_text(document)
            print(f'wrote {path.relative_to(ROOT)}')
    if stale:
        raise SystemExit('out of date (run scripts/build_home_i18n.py): ' + ', '.join(stale))
    if args.check:
        print('home translations current')


if __name__ == '__main__':
    main()
