/* Shared navigation and theme controls for the five main site pages. */
(() => {
  'use strict';
  const root = document.documentElement;
  const theme = document.getElementById('site-theme');
  const menu = document.getElementById('site-menu');
  const mobileNav = document.getElementById('mobile-nav');

  function syncTheme() {
    const light = root.classList.contains('light');
    theme.textContent = light ? '☾' : '☼';
    theme.setAttribute('aria-label', root.lang.startsWith('ja')
      ? `${light ? 'ダーク' : 'ライト'}テーマに切り替える`
      : `Switch to ${light ? 'dark' : 'light'} theme`);
    const darkSyntax = document.getElementById('hljs-dark');
    const lightSyntax = document.getElementById('hljs-light');
    if (darkSyntax && lightSyntax) {
      darkSyntax.disabled = light;
      lightSyntax.disabled = !light;
    }
    document.dispatchEvent(new CustomEvent('site:themechange', {detail: {theme: light ? 'light' : 'dark'}}));
  }
  theme.addEventListener('click', () => {
    root.classList.toggle('light');
    try { localStorage.setItem('theme', root.classList.contains('light') ? 'light' : 'dark'); } catch (_) {}
    syncTheme();
  });
  window.addEventListener('storage', event => {
    if (event.key === 'theme') {
      root.classList.toggle('light', event.newValue === 'light');
      syncTheme();
    }
  });
  syncTheme();

  function closeMenu(restoreFocus = false) {
    mobileNav.hidden = true;
    menu.setAttribute('aria-expanded', 'false');
    if (restoreFocus) menu.focus();
  }
  menu.addEventListener('click', () => {
    mobileNav.hidden = !mobileNav.hidden;
    menu.setAttribute('aria-expanded', String(!mobileNav.hidden));
  });
  mobileNav.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !mobileNav.hidden) closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  const desktop = matchMedia('(min-width: 1101px)');
  desktop.addEventListener('change', event => { if (event.matches) closeMenu(); });

  // The hero's small code preview is independent of the full chapter code boxes.
  const tablist = document.querySelector('.preview-tabs');
  if (tablist) {
    if (window.hljs) document.querySelectorAll('.preview-panels code').forEach(code => window.hljs.highlightElement(code));
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    function activate(tab, focus = false) {
      tabs.forEach(item => {
        const active = item === tab;
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
        document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
      });
      if (focus) tab.focus();
    }
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
      });
    });
  }
})();
