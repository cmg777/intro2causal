"""Browser regression checks for explicit Play and automatic playback pauses.

Run: uv run --with playwright python scripts/test_home_showcase.py
Install Chromium with `playwright install chromium` if needed. An existing browser
can be selected with PLAYWRIGHT_CHROMIUM_EXECUTABLE.
"""
from datetime import datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def verify(browser, url):
    def open_page(touch=False, reduced=False):
        context = browser.new_context(
            viewport={"width": 390 if touch else 1440, "height": 900 if touch else 1400},
            has_touch=touch,
            is_mobile=touch,
            reduced_motion="reduce" if reduced else "no-preference",
        )
        page = context.new_page()
        start = datetime(2026, 10, 23, tzinfo=timezone.utc)
        page.clock.install(time=start)
        page.clock.pause_at(start + timedelta(seconds=1))
        page.goto(url, wait_until="networkidle")
        return context, page

    def active(page):
        return page.locator('.method-scene.is-active').get_attribute('id')

    # The reported bug: Play must work without moving the pointer or blurring it.
    context, page = open_page()
    page.locator('#tab-rct').click()
    play = page.locator('#showcase-play')
    play.click()
    expect(page.locator('#showcase-status')).to_have_text('Changes every 10 seconds')
    expect(play).to_be_focused()
    page.clock.run_for(9999)
    assert active(page) == 'scene-rct'
    page.clock.run_for(1)
    assert active(page) == 'scene-regression'
    expect(play).to_be_focused()
    for method in ['iv', 'rd', 'did', 'rct']:
        page.clock.run_for(10000)
        assert active(page) == 'scene-' + method
    play.click()
    page.clock.run_for(20000)
    assert active(page) == 'scene-rct'
    play.click()

    # A later pointer entry pauses again; leaving resumes with a full interval.
    page.mouse.move(0, 0)
    page.mouse.move(1000, 300)
    expect(page.locator('#showcase-status')).to_contain_text('hover')
    page.clock.run_for(20000)
    assert active(page) == 'scene-rct'
    page.mouse.move(0, 0)
    page.clock.run_for(10000)
    assert active(page) == 'scene-regression'

    # New focus in the content pauses and manual selection remains stopped.
    page.locator('#tab-regression').focus()
    expect(page.locator('#showcase-status')).to_contain_text('explore')
    page.clock.run_for(20000)
    assert active(page) == 'scene-regression'
    page.keyboard.press('ArrowRight')
    assert active(page) == 'scene-iv'
    page.locator('#tab-iv').evaluate('(el) => el.blur()')
    page.clock.run_for(20000)
    assert active(page) == 'scene-iv'

    # Keyboard Play keeps focus and starts cycling, including under reduced motion.
    page.emulate_media(reduced_motion='reduce')
    play.focus()
    page.keyboard.press('Enter')
    expect(page.locator('#showcase-status')).to_have_text('Changes every 10 seconds')
    page.clock.run_for(10000)
    assert active(page) == 'scene-rd'
    expect(play).to_be_focused()
    assert page.locator('#scene-rd').evaluate('(el) => getComputedStyle(el).transitionDuration') == '0s'

    # Explicit Play still respects offscreen and browser-tab visibility suspension.
    page.evaluate('window.scrollTo({top: 2500, behavior: "instant"})')
    expect(page.locator('#showcase-status')).to_contain_text('out of view')
    page.clock.run_for(20000)
    assert active(page) == 'scene-rd'
    page.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
    expect(page.locator('#showcase-status')).to_have_text('Changes every 10 seconds')
    page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    page.clock.run_for(9999)
    assert active(page) == 'scene-rd'
    page.clock.run_for(1)
    assert active(page) == 'scene-did'
    page.evaluate("Object.defineProperty(document, 'hidden', {configurable:true, get:()=>true}); document.dispatchEvent(new Event('visibilitychange'))")
    page.clock.run_for(20000)
    assert active(page) == 'scene-did'
    page.evaluate("delete document.hidden; document.dispatchEvent(new Event('visibilitychange'))")
    page.clock.run_for(10000)
    assert active(page) == 'scene-rct'
    context.close()

    # Touch activation must work without a second tap elsewhere to clear focus.
    context, page = open_page(touch=True, reduced=True)
    page.locator('#showcase-play').tap()
    expect(page.locator('#showcase-status')).to_have_text('Changes every 10 seconds')
    page.clock.run_for(10000)
    assert active(page) == 'scene-regression'
    page.locator('#showcase-play').tap()
    page.clock.run_for(20000)
    assert active(page) == 'scene-regression'
    context.close()
    print('PASS: mouse, keyboard, touch, repeated cycling, Pause, new hover/focus, manual selection, reduced motion, offscreen and hidden-tab suspension')


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
