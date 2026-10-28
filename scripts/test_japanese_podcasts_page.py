"""Verify Japanese collection mappings, playback, transcript controls and fallbacks.

Run with: uv run --with playwright python scripts/test_japanese_podcasts_page.py
Optional: PLAYWRIGHT_CHROMIUM_EXECUTABLE=/path/to/chromium
"""
import json
import hashlib
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        # Match GitHub Pages byte-range support so browser media seeking is real.
        path = Path(self.translate_path(self.path))
        if path.suffix != '.mp3' or not path.is_file():
            return super().do_GET()
        size = path.stat().st_size
        start, end = 0, size - 1
        header = self.headers.get('Range')
        if header:
            first, last = header.removeprefix('bytes=').split('-', 1)
            start, end = int(first or 0), min(int(last or end), end)
        self.send_response(206 if header else 200)
        self.send_header('Content-Type', 'audio/mpeg')
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(end - start + 1))
        if header:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        try:
            with path.open('rb') as audio:
                audio.seek(start)
                remaining = end - start + 1
                while remaining:
                    chunk = audio.read(min(65536, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

def verify(browser, base):
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + '/podcasts.html')
    page.get_by_role('link', name='Explore Japanese version').click()
    expect(page.locator('html')).to_have_attribute('lang', 'ja')
    expect(page.locator('.podcast-player.enhanced')).to_have_count(6)
    assert page.locator('audio').count() == 6
    assert page.locator('.episode-art').count() == 6
    # Full translated maps must use their own assets and retain landscape geometry.
    full_maps = page.locator('.full-mindmap img')
    assert full_maps.count() == 7  # Six chapter cards and the Chapter 1 hero.
    manifest = json.loads((ROOT / 'mindmaps/ja/manifest.json').read_text())
    assert [entry['chapter'] for entry in manifest['chapters']] == list(range(1, 7))
    for entry in manifest['chapters']:
        art = page.locator(f"#chapter-{entry['chapter']} .episode-art")
        assert art.get_attribute('href') == entry['full_image']
        assert art.locator('img').get_attribute('src') == entry['web_image']
        for path_key, hash_key in [('english_source', 'english_source_sha256'), ('full_image', 'full_image_sha256'), ('web_image', 'web_image_sha256')]:
            assert hashlib.sha256((ROOT / entry[path_key]).read_bytes()).hexdigest() == entry[hash_key]
        assert (ROOT / entry['prompt']).is_file()
    assert page.locator('.featured-art img').get_attribute('src') == manifest['chapters'][0]['web_image']
    assert page.locator('a[href*="spotify-jpn/artwork"], img[src*="spotify-jpn/artwork"]').count() == 0
    for image in full_maps.all():
        image.scroll_into_view_if_needed()
        expect(image).to_be_visible()
        assert '/full/' in image.get_attribute('src')
        page.wait_for_function('(img) => img.complete && img.naturalWidth > 0', arg=image.element_handle())
        assert image.evaluate('(img) => img.naturalWidth / img.naturalHeight > 1.7')
        assert image.evaluate('(img) => Math.abs(img.width / img.height - img.naturalWidth / img.naturalHeight) < 0.02')
    assert page.locator('#chapter-1 .episode-art').get_attribute('href').startswith('mindmaps/ja/images/')
    assert page.locator('.episode-pending').count() == 0
    assert '準備中' not in page.locator('main').inner_text()
    expect(page.locator('.podcast-status')).to_have_text([''] * 6)
    state = json.loads((ROOT / 'publishing/spotify-jpn/state.json').read_text())
    for i in range(1, 7):
        player = page.locator(f'#chapter-{i}-podcast')
        transcript_path = player.get_attribute('data-podcast')
        data = json.loads((ROOT / transcript_path).read_text())
        slug = Path(transcript_path).stem
        assert player.locator('.podcast-passages button > span:last-child').all_text_contents() == [s['text'] for s in data['segments']]
        assert player.locator('.podcast-action-link').nth(1).get_attribute('href') == state['episodes'][slug]['public_url']
        assert slug in player.locator('source').get_attribute('src')
        lesson = ROOT / f'mindmaps-podcast/ja/study/{slug}.html'
        lesson_links = player.locator(f'.podcast-action-link[href="mindmaps-podcast/ja/study/{slug}.html"]')
        assert lesson_links.count() == (1 if lesson.exists() else 0)
        assert player.locator('.podcast-now').inner_text() == '現在：オープニング'
        player.locator('.podcast-play').click()
        expect(player.locator('.podcast-play')).to_have_attribute('aria-label', '一時停止')
        page.wait_for_function('(i) => document.querySelector(`#chapter-${i}-podcast audio`).currentTime > 0.3', arg=i)
        player.locator('.podcast-play').click()
        player.locator('.podcast-transcript-toggle').click()
        expect(player.locator('.podcast-transcript')).to_be_visible()
        player.locator('.podcast-chapters button').nth(1).click()
        page.wait_for_function('([i,t]) => Math.abs(document.querySelector(`#chapter-${i}-podcast audio`).currentTime-t)<1', arg=[i, data['sections'][1]['start']])
        assert player.locator('audio').evaluate('(a) => a.paused')
        player.locator('[data-speed]').click()
        assert player.locator('audio').evaluate('(a) => a.playbackRate') == 1.25
        player.locator('.podcast-passages').dispatch_event('wheel')
        expect(player.locator('[data-follow]')).not_to_be_checked()
    # Opening a static transcript does not interrupt playback.
    player = page.locator('#chapter-1-podcast')
    player.locator('.podcast-play').click()
    with page.expect_popup() as popup:
        player.locator('.podcast-action-link').first.click()
    popup.value.wait_for_load_state()
    assert popup.value.locator('html').get_attribute('lang') == 'ja'
    assert not player.locator('audio').evaluate('(a) => a.paused')
    popup.value.close()
    # Starting another chapter pauses only the other enhanced players.
    fifth = page.locator('#chapter-5 audio')
    page.locator('#chapter-5 .podcast-play').click()
    page.wait_for_function('document.querySelector("#chapter-5 audio").currentTime > 0.3')
    assert player.locator('audio').evaluate('(a) => a.paused')
    player.locator('.podcast-play').click()
    assert fifth.evaluate('(a) => a.paused')
    player.locator('.podcast-play').click()
    # Validate all local resource and chapter targets, including full-size mind maps.
    links = page.locator('[href], [src], [data-podcast]').evaluate_all('(els) => els.flatMap(e => [e.getAttribute("href"),e.getAttribute("src"),e.getAttribute("data-podcast")]).filter(Boolean)')
    for url in links:
        if url.startswith(('https:', 'http:', 'data:')):
            continue
        if url.startswith('#'):
            assert page.locator(url).count() == 1, url
        else:
            assert (ROOT / url.split('#')[0].split('?')[0]).is_file(), url
    # Japanese text fits both themes at narrow mobile and desktop sizes.
    for width in [320, 390, 768, 1101, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        for theme in ['light', 'dark']:
            page.evaluate('(theme) => document.documentElement.classList.toggle("light", theme === "light")', theme)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, theme)
    assert not errors, errors
    # English remains enhanced after the shared runtime localization.
    page.goto(base + '/podcasts.html')
    expect(page.locator('.podcast-player.enhanced')).to_have_count(6)
    expect(page.locator('#chapter-1-podcast .podcast-play')).to_have_attribute('aria-label', 'Play podcast')
    page.close()
    # Transcript fetch failures leave native playback and static links available.
    page = browser.new_page()
    page.route('**/ja/transcripts/*.json', lambda route: route.abort())
    page.goto(base + '/podcasts-ja.html')
    expect(page.locator('#chapter-1-podcast .podcast-status')).to_contain_text('読み込めません')
    expect(page.locator('#chapter-1-podcast audio')).to_be_visible()
    expect(page.locator('#chapter-1-podcast .podcast-action-link').first).to_be_visible()
    page.close()
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(base + '/podcasts-ja.html')
    assert page.locator('audio[controls]').count() == 6
    expect(page.locator('#chapter-1-podcast audio')).to_be_visible()
    page.locator('#chapter-1-podcast .podcast-action-link').first.get_attribute('href')
    context.close()
    print('PASS: Japanese mappings, playback, transcript controls, English regression, responsive layout and fallbacks')

if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            options = {'headless': True}
            if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
                options['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
            browser = playwright.chromium.launch(**options)
            verify(browser, f'http://127.0.0.1:{server.server_port}')
            browser.close()
    finally:
        server.shutdown()
