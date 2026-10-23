/* Progressive enhancement for the homepage; no changes to the shared player. */
(() => {
  'use strict';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const showcase = document.querySelector('.method-showcase');
  if (showcase) {
    const scenes = [...showcase.querySelectorAll('.method-scene')];
    const tabs = [...showcase.querySelectorAll('[role="tab"]')];
    const playButton = showcase.querySelector('#showcase-play');
    const status = showcase.querySelector('#showcase-status');
    const count = showcase.querySelector('.showcase-count');
    let current = 0;
    let playing = !reducedMotion.matches;
    let hovered = showcase.matches(':hover');
    let inView = false;
    let timer;

    // Every scene contributes to the grid height, even when visually hidden.
    // Inactive scenes are inert and excluded from the accessibility tree.
    showcase.classList.add('showcase-enhanced');
    scenes.forEach((scene, index) => {
      scene.setAttribute('role', 'tabpanel');
      scene.setAttribute('aria-labelledby', tabs[index].id);
      scene.setAttribute('aria-hidden', String(index !== current));
      scene.inert = index !== current;
      scene.tabIndex = index === current ? 0 : -1;
      scene.hidden = false;
    });
    showcase.querySelector('.showcase-controls').hidden = false;

    function updatePlayback() {
      clearTimeout(timer);
      const focused = showcase.contains(document.activeElement);
      playButton.querySelector('[data-playback-label]').textContent = playing ? 'Pause' : 'Play';
      playButton.querySelector('[data-playback-icon]').textContent = playing ? 'Ⅱ' : '▷';
      playButton.setAttribute('aria-label', `${playing ? 'Pause' : 'Start'} automatic method cycling`);
      status.textContent = !playing ? 'Choose a method, or press Play'
        : document.hidden ? 'Paused while the tab is hidden'
        : !inView ? 'Paused while out of view'
        : focused ? 'Paused while you explore'
        : hovered ? 'Paused while you hover'
        : 'Changes every 10 seconds';
      // Resume with a fresh interval; no queued transitions or catch-up jumps.
      if (playing && inView && !document.hidden && !hovered && !focused) {
        timer = setTimeout(() => {
          selectScene((current + 1) % scenes.length);
          updatePlayback();
        }, 10000);
      }
    }

    function selectScene(index) {
      current = index;
      scenes.forEach((scene, i) => {
        const active = i === current;
        scene.classList.toggle('is-active', active);
        scene.classList.remove('assignment-playing');
        scene.setAttribute('aria-hidden', String(!active));
        scene.inert = !active;
        scene.tabIndex = active ? 0 : -1;
        tabs[i].setAttribute('aria-selected', String(active));
        tabs[i].tabIndex = active ? 0 : -1;
      });
      if (!reducedMotion.matches) {
        void scenes[current].offsetWidth;
        scenes[current].classList.add('assignment-playing');
      }
      count.textContent = `${String(current + 1).padStart(2, '0')} / 05`;
      // The image is decorative: a late or failed load never blocks the scene.
      const nextImage = scenes[(current + 1) % scenes.length].querySelector('img');
      nextImage.loading = 'eager';
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => {
        playing = false;
        selectScene(index);
        updatePlayback();
      });
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        playing = false;
        selectScene(next);
        tabs[next].focus({preventScroll: true});
        updatePlayback();
      });
    });
    playButton.addEventListener('click', () => {
      playing = !playing;
      updatePlayback();
    });
    showcase.addEventListener('pointerenter', event => {
      if (event.pointerType === 'touch') return;
      hovered = true;
      updatePlayback();
    });
    showcase.addEventListener('pointerleave', () => {
      hovered = false;
      updatePlayback();
    });
    showcase.addEventListener('focusin', updatePlayback);
    showcase.addEventListener('focusout', () => queueMicrotask(updatePlayback));
    document.addEventListener('visibilitychange', updatePlayback);
    reducedMotion.addEventListener('change', () => {
      // Turning reduced motion on stops cycling; turning it off does not opt back in.
      if (reducedMotion.matches) playing = false;
      scenes.forEach(scene => scene.classList.remove('assignment-playing'));
      updatePlayback();
    });
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting && entries[0].intersectionRatio >= .15;
        updatePlayback();
      }, {threshold: [0, .15]});
      observer.observe(showcase);
    } else {
      inView = true;
    }
    selectScene(0);
    updatePlayback();
  }

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
