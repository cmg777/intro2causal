"""Check hero fit on laptops and unclipped, scrollable layouts on smaller screens.

Run: uv run --with playwright python scripts/test_home_layout.py
Optionally set PLAYWRIGHT_CHROMIUM_EXECUTABLE to an installed Chromium binary.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import os
from threading import Thread

from playwright.sync_api import expect, sync_playwright
from test_home_showcase import QuietHandler, ROOT

# Include short laptops, both sides of the stacking breakpoint, tablets, and phones.
VIEWPORTS = [
    (1280, 720), (1366, 768), (1440, 900), (1536, 864), (1920, 950),
    (1920, 1080), (1001, 768), (1000, 768), (1024, 768), (834, 1194),
    (768, 1024), (390, 844), (375, 667), (320, 568), (844, 390), (1280, 600),
]


def verify(browser, url):
    page = browser.new_page(reduced_motion='reduce')
    page.goto(url, wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    for theme in ['dark', 'light']:
        page.evaluate('(light) => document.documentElement.classList.toggle("light", light)', theme == 'light')
        for width, height in VIEWPORTS:
            page.set_viewport_size({'width': width, 'height': height})
            page.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
            label = f'{theme} {width}x{height}'
            hero = page.locator('.home-hero').bounding_box()
            author = page.locator('.hero-author').bounding_box()
            card = page.locator('.method-showcase').bounding_box()
            if width > 1000 and height >= 720:
                assert hero['y'] + hero['height'] <= height, f'{label}: hero below viewport'
            if width <= 1000:
                assert author['y'] + author['height'] <= card['y'], f'{label}: credits must precede carousel'
            # Check child bounds as well: overflow:clip can hide a layout bug from scrollWidth.
            overflow = page.locator('.home-hero').evaluate('''hero => [...hero.querySelectorAll('*')]
                .filter(el => !el.closest('svg, .hero-orbit, .scene-art'))
                .filter(el => {const r = el.getBoundingClientRect();
                    return r.width && (r.left < -1 || r.right > innerWidth + 1);})
                .map(el => el.className)''')
            assert not overflow, f'{label}: horizontal overflow {overflow}'
            for method in ['rct', 'regression', 'iv', 'rd', 'did']:
                page.locator(f'#tab-{method}').click()
                scene = page.locator(f'#scene-{method}')
                expect(scene).to_have_attribute('aria-hidden', 'false')
                note = scene.locator('.scene-note').bounding_box()
                controls = page.locator('.showcase-controls').bounding_box()
                assert note['y'] + note['height'] <= controls['y'], f'{label} {method}: caption clipped'
                assert abs(page.locator('.method-showcase').bounding_box()['height'] - card['height']) < 1, f'{label}: carousel jumps'
            # Credits and controls remain reachable with ordinary page scrolling.
            for selector in ['.hero-author a', '#showcase-play', '.method-scene.is-active .scene-chapter']:
                target = page.locator(selector).first
                target.scroll_into_view_if_needed()
                expect(target).to_be_in_viewport()
                assert target.evaluate('''el => {const r=el.getClientRects()[0];
                    return el.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));}'''), f'{label}: {selector} obscured'
    page.close()
    print(f'PASS: all five slides, credits, controls, and overflow at {len(VIEWPORTS)} sizes in both themes')


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            executable = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
            browser = playwright.chromium.launch(**({'executable_path': executable} if executable else {}))
            try:
                verify(browser, f'http://127.0.0.1:{server.server_port}/')
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
