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
    // Showcase copy for the English, Spanish and Japanese home pages.
    const lang = document.documentElement.lang.slice(0, 2);
    const copies = {
      en: {pause: 'Pause', play: 'Play', pauseCycling: 'Pause automatic method cycling', startCycling: 'Start automatic method cycling',
        choose: 'Choose a method, or press Play', hidden: 'Paused while the tab is hidden', away: 'Paused while out of view',
        exploring: 'Paused while you explore', hovering: 'Paused while you hover', cycling: 'Changes every 10 seconds'},
      es: {pause: 'Pausar', play: 'Reproducir', pauseCycling: 'Pausar el cambio automático de métodos', startCycling: 'Iniciar el cambio automático de métodos',
        choose: 'Elige un método o presiona Reproducir', hidden: 'En pausa mientras la pestaña está oculta', away: 'En pausa mientras no está a la vista',
        exploring: 'En pausa mientras exploras', hovering: 'En pausa mientras pasas el cursor', cycling: 'Cambia cada 10 segundos'},
      ja: {pause: '一時停止', play: '再生', pauseCycling: '手法の自動切り替えを一時停止', startCycling: '手法の自動切り替えを開始',
        choose: '手法を選ぶか、再生を押してください', hidden: 'タブが非表示のため一時停止中', away: '画面外のため一時停止中',
        exploring: '操作中のため一時停止中', hovering: 'カーソルを合わせているため一時停止中', cycling: '10秒ごとに切り替わります'},
    };
    const copy = copies[lang] || copies.en;
    let current = 0;
    let playing = !reducedMotion.matches;
    let hovered = showcase.matches(':hover');
    let resumeHovered = false;
    let resumeFocused = false;
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
      const focused = showcase.contains(document.activeElement)
        && !(resumeFocused && document.activeElement === playButton);
      const hoverPaused = hovered && !resumeHovered;
      playButton.querySelector('[data-playback-label]').textContent = playing ? copy.pause : copy.play;
      playButton.querySelector('[data-playback-icon]').textContent = playing ? 'Ⅱ' : '▷';
      playButton.setAttribute('aria-label', playing ? copy.pauseCycling : copy.startCycling);
      status.textContent = !playing ? copy.choose
        : document.hidden ? copy.hidden
        : !inView ? copy.away
        : focused ? copy.exploring
        : hoverPaused ? copy.hovering
        : copy.cycling;
      // Resume with a fresh interval; no queued transitions or catch-up jumps.
      if (playing && inView && !document.hidden && !hoverPaused && !focused) {
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
      // Explicit Play overrides the hover/focus that activated this button.
      // Keep keyboard focus in place; a later hover or focus starts a new pause.
      resumeHovered = playing && hovered;
      resumeFocused = playing && document.activeElement === playButton;
      updatePlayback();
    });
    showcase.addEventListener('pointerenter', event => {
      if (event.pointerType === 'touch') return;
      hovered = true;
      resumeHovered = false;
      updatePlayback();
    });
    showcase.addEventListener('pointerleave', () => {
      hovered = false;
      resumeHovered = false;
      updatePlayback();
    });
    showcase.addEventListener('focusin', () => {
      resumeFocused = false;
      updatePlayback();
    });
    showcase.addEventListener('focusout', () => {
      resumeFocused = false;
      queueMicrotask(updatePlayback);
    });
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
