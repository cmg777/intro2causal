"""Browser checks for the English, Spanish and Japanese home pages and the language switcher.

Run: uv run --with playwright python scripts/test_home_i18n.py
Optionally set PLAYWRIGHT_CHROMIUM_EXECUTABLE to an installed Chromium binary.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import os
from threading import Thread

from playwright.sync_api import expect, sync_playwright
from test_home_showcase import QuietHandler, ROOT

PAGES = {'en': 'index.html', 'es': 'index-es.html', 'ja': 'index-ja.html'}
MAPS = {'en': 'book/images/ch0', 'es': 'assets/home-es/full/', 'ja': 'assets/podcasts-ja/full/'}


def open_page(browser, url, locale='en-US', stored=None, width=1440):
    context = browser.new_context(locale=locale, viewport={'width': width, 'height': 900})
    if stored:
        context.add_init_script(f"try{{localStorage.setItem('lang','{stored}')}}catch(e){{}}")
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda message: message.type == 'error' and errors.append(message.text))
    page.goto(url, wait_until='networkidle')
    return context, page, errors


def verify(browser, base):
    # Each page loads cleanly, declares its language, and uses its own mind maps and players.
    for lang, name in PAGES.items():
        context, page, errors = open_page(browser, base + name)
        assert page.evaluate('document.documentElement.lang') == lang
        expect(page.locator(f'.site-nav .lang-switch a[data-lang="{lang}"]')).to_have_attribute('aria-current', 'true')
        maps = page.locator('.chapter-thumb img').evaluate_all('imgs => imgs.map(img => img.getAttribute("src"))')
        assert len(maps) == 6 and all(src.startswith(MAPS[lang]) for src in maps), maps
        page.locator('.chapter-thumb img').last.scroll_into_view_if_needed()
        page.wait_for_function('[...document.querySelectorAll(".chapter-thumb img")].every(i => i.complete && i.naturalWidth > 0)')
        podcasts = page.locator('.podcast-player').evaluate_all('ps => ps.map(p => p.dataset.podcast)')
        assert all(('/ja/' in src) == (lang == 'ja') for src in podcasts), podcasts
        page.locator('#chapter-1 [data-podcast-toggle]').click()
        expect(page.locator('#chapter-1-podcast .podcast-passages button').first).to_be_attached(timeout=10000)
        assert not errors, f'{name}: {errors}'
        context.close()
        print(f'PASS {name}: lang, maps, players, no console errors')

    # index.html follows a stored choice, else the browser language; translated pages never redirect.
    for locale, expected in [('es-MX', 'index-es.html'), ('ja-JP', 'index-ja.html'), ('en-US', 'index.html'), ('fr-FR', 'index.html')]:
        context, page, _ = open_page(browser, base + 'index.html', locale=locale)
        assert page.url.endswith(expected), (locale, page.url)
        context.close()
    context, page, _ = open_page(browser, base + 'index.html', locale='es-MX', stored='en')
    assert page.url.endswith('index.html'), page.url
    context.close()
    context, page, _ = open_page(browser, base + 'index-ja.html', locale='es-MX')
    assert page.url.endswith('index-ja.html'), 'translated pages must never redirect'
    context.close()
    print('PASS redirect: es/ja first visits, stored choice, no redirect from translated pages')

    # Clicking a pill navigates and remembers the choice, so returning to index.html stays put.
    context, page, _ = open_page(browser, base + 'index.html', locale='ja-JP')
    page.locator('.site-nav .lang-switch a[data-lang="en"]').click()
    page.wait_for_url('**/index.html')
    assert page.evaluate("localStorage.getItem('lang')") == 'en'
    page.locator('.site-nav .lang-switch a[data-lang="es"]').click()
    page.wait_for_url('**/index-es.html')
    page.goto(base + 'index.html', wait_until='networkidle')
    assert page.url.endswith('index-es.html'), 'a stored es choice should send index.html to index-es.html'
    context.close()

    # On phones the pills move into the menu.
    context, page, _ = open_page(browser, base + 'index-es.html', width=375)
    expect(page.locator('.site-nav .lang-switch')).to_be_hidden()
    page.locator('#site-menu').click()
    expect(page.locator('#mobile-nav .lang-switch-mobile')).to_be_visible()
    page.locator('#mobile-nav .lang-switch-mobile a[data-lang="ja"]').click()
    page.wait_for_url('**/index-ja.html')
    context.close()
    print('PASS switcher: desktop pills, mobile menu pills, remembered choice')


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
