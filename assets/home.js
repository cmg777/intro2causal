/* Progressive enhancement for the homepage; no changes to the shared player. */
(() => {
  'use strict';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const scene = document.querySelector('.comparison-scene');
  const replay = document.getElementById('replay-assignment');
  let animationTimer;
  function animateAssignment() {
    clearTimeout(animationTimer);
    scene.classList.remove('assignment-playing');
    if (reducedMotion.matches) return;
    // Restart the finite CSS animation when the reader requests a replay.
    void scene.offsetWidth;
    scene.classList.add('assignment-playing');
    animationTimer = setTimeout(() => scene.classList.remove('assignment-playing'), 3100);
  }
  replay.hidden = reducedMotion.matches;
  replay.addEventListener('click', animateAssignment);
  reducedMotion.addEventListener('change', () => {
    replay.hidden = reducedMotion.matches;
    if (reducedMotion.matches) scene.classList.remove('assignment-playing');
  });
  const sceneObserver = new IntersectionObserver(entries => {
    if (entries.some(entry => entry.isIntersecting)) {
      animateAssignment();
      sceneObserver.disconnect();
    }
  }, {threshold: .35});
  sceneObserver.observe(scene);

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (!reducedMotion.matches) entry.target.classList.add('home-reveal');
      revealObserver.unobserve(entry.target);
    });
  }, {threshold: .08});
  document.querySelectorAll('.learning-steps li, .chapter-card, .home-practice').forEach(item => revealObserver.observe(item));

  // Complete the existing lightbox/video functions with modal semantics and focus handling.
  let activeDialog = null;
  let returnFocus = null;
  const main = document.querySelector('main');
  const header = document.querySelector('.site-header');
  const footer = document.querySelector('.home-footer');
  const outside = [main, header, footer, document.getElementById('back-to-top')];
  function activateDialog(id) {
    returnFocus = document.activeElement;
    activeDialog = document.getElementById(id);
    outside.forEach(item => { if (item) item.inert = true; });
    activeDialog.querySelector('button').focus();
  }
  function deactivateDialog(id) {
    if (!activeDialog || activeDialog.id !== id) return;
    activeDialog = null;
    outside.forEach(item => { if (item) item.inert = false; });
    if (returnFocus?.isConnected) returnFocus.focus({preventScroll: true});
  }
  for (const [openName, closeName, id, titleId] of [
    ['openVideo', 'closeVideo', 'video-modal', 'video-title'],
    ['openImage', 'closeImage', 'image-modal', 'image-modal-title']
  ]) {
    const dialog = document.getElementById(id);
    dialog.setAttribute('role', 'dialog');
    dialog.setAttribute('aria-modal', 'true');
    dialog.setAttribute('aria-labelledby', titleId);
    const originalOpen = window[openName];
    const originalClose = window[closeName];
    window[openName] = (...args) => {
      originalOpen(...args);
      if (id === 'video-modal') document.getElementById('video-iframe').title = args[1];
      activateDialog(id);
    };
    window[closeName] = (...args) => {
      originalClose(...args);
      deactivateDialog(id);
    };
  }
  document.addEventListener('keydown', event => {
    if (!activeDialog || event.key !== 'Tab') return;
    const focusable = [...activeDialog.querySelectorAll('button, a[href], iframe')];
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
})();
