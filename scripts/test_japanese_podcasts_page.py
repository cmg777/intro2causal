"""Verify Japanese collection mappings, playback, transcript controls and fallbacks.

Run with: uv run --with playwright python scripts/test_japanese_podcasts_page.py
Optional: PLAYWRIGHT_CHROMIUM_EXECUTABLE=/path/to/chromium
"""
import json
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
    expect(page.locator('.podcast-player.enhanced')).to_have_count(4)
    assert page.locator('audio').count() == 5
    assert page.locator('.episode-art').count() == 6
    assert page.locator('#chapter-6 audio, #chapter-6 [data-podcast]').count() == 0
    assert page.locator('#chapter-5 .podcast-action-link').count() == 0
    expect(page.locator('#chapter-5')).to_contain_text('文字起こしは準備中')
    expect(page.locator('.podcast-status')).to_have_text([''] * 4)
    state = json.loads((ROOT / 'publishing/spotify-jpn/state.json').read_text())
    for i in range(1, 5):
        player = page.locator(f'#chapter-{i}-podcast')
        transcript_path = player.get_attribute('data-podcast')
        data = json.loads((ROOT / transcript_path).read_text())
        slug = Path(transcript_path).stem
        assert player.locator('.podcast-passages button > span:last-child').all_text_contents() == [s['text'] for s in data['segments']]
        assert player.locator('.podcast-action-link').nth(1).get_attribute('href') == state['episodes'][slug]['public_url']
        assert slug in player.locator('source').get_attribute('src')
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
    # Native Chapter 5 playback pauses an enhanced player and vice versa.
    fifth = page.locator('#chapter-5 audio')
    fifth.evaluate('(a) => a.play()')
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
    assert page.locator('audio[controls]').count() == 5
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
