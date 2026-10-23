/* Offline-generated transcript; the player needs no third-party service. */
(() => {
  const japanese = document.documentElement.lang.startsWith('ja');
  const text = (english, translated) => japanese ? translated : english;
  const playError = text('Audio could not play.', '音声を再生できませんでした。');
  async function startPlayback(audio, status) {
    document.querySelectorAll('.podcast-player audio, .episode-pending audio').forEach(other => { if (other !== audio) other.pause(); });
    try {
      // Call play directly from the click, without waiting for transcript loading.
      await audio.play();
      if (status.textContent.startsWith(playError)) status.textContent = '';
    } catch (error) {
      // Closing or switching players can cancel a pending playback request.
      if (error.name !== 'AbortError') {
        status.textContent = text('Audio could not play. Please try again. You can also read the transcript.', '音声を再生できませんでした。もう一度お試しください。文字起こしもご利用いただけます。');
      }
    }
  }
  // Bind playback and error handling before transcript fetches, including native fallback.
  document.querySelectorAll('[data-podcast]').forEach(player => {
    const audio = player.querySelector('audio');
    const status = document.createElement('p');
    status.className = 'podcast-audio-status';
    status.setAttribute('role', 'status');
    player.append(status);
    audio.addEventListener('play', () => {
      document.querySelectorAll('.podcast-player audio, .episode-pending audio').forEach(other => { if (other !== audio) other.pause(); });
    });
    audio.addEventListener('playing', () => { status.textContent = ''; });
    audio.addEventListener('error', () => { status.textContent = text('Audio is unavailable. Please try again later, or use the Spotify link.', '音声を読み込めません。後でもう一度お試しいただくか、Spotifyのリンクをご利用ください。'); });
  });
  document.querySelectorAll('.episode-pending audio').forEach(audio => {
    audio.addEventListener('play', () => {
      document.querySelectorAll('.podcast-player audio, .episode-pending audio').forEach(other => {
        if (other !== audio) other.pause();
      });
    });
  });
  document.querySelectorAll('[data-podcast-start]').forEach(button => {
    button.addEventListener('click', () => {
      const player = document.getElementById(button.dataset.podcastStart);
      // Call play in the click handler, even if transcript enhancement is still loading.
      startPlayback(player.querySelector('audio'), player.querySelector('.podcast-audio-status'));
      player.setAttribute('tabindex', '-1');
      player.focus({ preventScroll: true });
      player.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
    });
  });
  document.querySelectorAll('[data-podcast-toggle]').forEach(button => {
    const player = document.getElementById(button.getAttribute('aria-controls'));
    const audio = player.querySelector('audio');
    const status = player.querySelector('.podcast-audio-status');
    const close = () => {
      button.setAttribute('aria-expanded', 'false');
      player.hidden = true;
      player.querySelector('audio').pause();
    };
    button.addEventListener('click', () => {
      const opening = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(opening));
      player.hidden = !opening;
      if (opening) startPlayback(audio, status);
      else audio.pause();
    });
    player.querySelector('.podcast-close').addEventListener('click', () => {
      close();
      button.focus();
    });
  });
  const formatTime = seconds => {
    const value = Math.max(0, Math.floor(seconds || 0));
    return `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
  };
  document.querySelectorAll('[data-podcast]').forEach(async player => {
    const audio = player.querySelector('audio');
    const status = player.querySelector('.podcast-status');
    try {
      const response = await fetch(player.dataset.podcast);
      if (!response.ok) throw new Error('Transcript unavailable');
      const episode = await response.json();
      const play = player.querySelector('.podcast-play');
      const seek = player.querySelector('[data-seek]');
      const elapsed = player.querySelector('[data-elapsed]');
      const duration = player.querySelector('[data-duration]');
      const transcript = player.querySelector('.podcast-passages');
      const transcriptPanel = player.querySelector('.podcast-transcript');
      const transcriptToggle = player.querySelector('.podcast-transcript-toggle');
      const follow = player.querySelector('[data-follow]');
      player.querySelector('[data-episode-minutes]').textContent = Math.round(episode.duration / 60);
      let currentPassage = -1;
      let currentSection = -1;
      let pendingSeek = null;
      let following = follow.checked;
      const sectionName = (section, index) => !japanese && index > 0 && index < episode.sections.length - 1 ? `Part ${index} · ${section.title}` : section.title;
      const chapterButtons = episode.sections.map((section, index) => {
        const button = document.createElement('button');
        button.type = 'button';
        const time = document.createElement('time');
        time.textContent = formatTime(section.start);
        const title = document.createElement('span');
        title.textContent = sectionName(section, index);
        button.append(time, title);
        button.setAttribute('aria-label', `${section.title}, ${formatTime(section.start)}`);
        button.addEventListener('click', () => jump(section.start));
        player.querySelector('.podcast-chapters').append(button);
        if (index > 0) {
          const cut = document.createElement('span');
          cut.style.left = `${100 * section.start / episode.duration}%`;
          player.querySelector('.podcast-cuts').append(cut);
        }
        return button;
      });
      const passageButtons = episode.segments.map((segment, i) => {
        const section = episode.sections.find(s => s.segment === i);
        if (section) {
          const heading = document.createElement('h6');
          heading.textContent = section.title;
          transcript.append(heading);
        }
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.speaker = segment.speaker;
        const time = document.createElement('time');
        time.textContent = formatTime(segment.start);
        const text = document.createElement('span');
        const speaker = document.createElement('span');
        speaker.className = 'podcast-speaker';
        speaker.append(japanese ? ({ HOST: '司会', ECONOMIST: '先生' }[segment.speaker] || segment.speaker) : segment.speaker, time);
        text.textContent = segment.text;
        button.append(speaker, text);
        button.addEventListener('click', () => jump(segment.start));
        transcript.append(button);
        return button;
      });
      function jump(time) {
        const target = Math.max(0, Math.min(audio.duration || episode.duration, time));
        if (audio.readyState === 0) {
          pendingSeek = target;
          audio.load();
        } else audio.currentTime = target;
        // Seeking preserves the student's choice to listen or read while paused.
        update(target);
      }
      function update(time = audio.currentTime) {
        const total = Number.isFinite(audio.duration) ? audio.duration : episode.duration;
        seek.max = total;
        seek.value = time;
        seek.setAttribute('aria-valuetext', text(`${formatTime(time)} of ${formatTime(total)}`, `${formatTime(total)}中 ${formatTime(time)}`));
        elapsed.textContent = formatTime(time);
        duration.textContent = formatTime(total);
        player.querySelector('[data-progress]').style.width = `${100 * time / total}%`;
        // Recordings may begin with silence before the first timed section.
        const s = Math.max(0, episode.sections.findLastIndex(section => section.start <= time));
        if (s !== currentSection) {
          chapterButtons[currentSection]?.removeAttribute('aria-current');
          chapterButtons[s]?.setAttribute('aria-current', 'true');
          player.querySelector('.podcast-now').textContent = `${text('Now: ', '現在：')}${sectionName(episode.sections[s], s)}`;
          currentSection = s;
        }
        const p = episode.segments.findLastIndex(segment => segment.start <= time);
        const active = p >= 0 && time < episode.segments[p].end ? p : -1;
        if (active !== currentPassage) {
          passageButtons[currentPassage]?.removeAttribute('aria-current');
          passageButtons[active]?.setAttribute('aria-current', 'true');
          currentPassage = active;
          scrollToPassage();
        }
      }
      function scrollToPassage() {
        if (!following || transcriptPanel.hidden || currentPassage < 0) return;
        const button = passageButtons[currentPassage];
        const container = transcript.getBoundingClientRect();
        const rect = button.getBoundingClientRect();
        // Scroll only the transcript, never the page the student is reading.
        transcript.scrollTop += rect.top - container.top - transcript.clientHeight / 3;
      }
      const stopFollowing = () => { following = false; follow.checked = false; };
      transcript.addEventListener('wheel', stopFollowing, { passive: true });
      transcript.addEventListener('touchstart', stopFollowing, { passive: true });
      transcript.addEventListener('keydown', event => {
        if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End'].includes(event.key)) stopFollowing();
      });
      follow.addEventListener('change', () => { following = follow.checked; scrollToPassage(); });
      transcriptToggle.addEventListener('click', () => {
        const opening = transcriptPanel.hidden;
        transcriptPanel.hidden = !opening;
        transcriptToggle.setAttribute('aria-expanded', String(opening));
        transcriptToggle.querySelector('span').textContent = opening ? text('Hide transcript', '文字起こしを閉じる') : text('Read along', '文字起こしを表示');
        if (opening) scrollToPassage();
      });
      play.addEventListener('click', () => {
        if (!audio.paused) return audio.pause();
        startPlayback(audio, player.querySelector('.podcast-audio-status'));
      });
      function updatePlay() {
        const playing = !audio.paused;
        play.setAttribute('aria-label', playing ? text('Pause podcast', '一時停止') : text('Play podcast', '再生'));
        play.setAttribute('aria-pressed', String(playing));
        // SVG elements do not reliably reflect the HTML `hidden` property.
        play.querySelector('[data-play-icon]').toggleAttribute('hidden', playing);
        play.querySelector('[data-pause-icon]').toggleAttribute('hidden', !playing);
      }
      audio.addEventListener('play', updatePlay);
      audio.addEventListener('pause', updatePlay);
      audio.addEventListener('playing', updatePlay);
      audio.addEventListener('ended', updatePlay);
      audio.addEventListener('timeupdate', () => update());
      audio.addEventListener('progress', () => {
        if (audio.buffered.length) player.querySelector('[data-buffer]').style.width = `${100 * audio.buffered.end(audio.buffered.length - 1) / episode.duration}%`;
      });
      audio.addEventListener('loadedmetadata', () => {
        if (pendingSeek !== null) { audio.currentTime = pendingSeek; pendingSeek = null; }
        update();
      });
      seek.addEventListener('input', () => jump(Number(seek.value)));
      player.querySelectorAll('[data-skip]').forEach(button => button.addEventListener('click', () => jump((pendingSeek ?? audio.currentTime) + Number(button.dataset.skip))));
      const speeds = [1, 1.25, 1.5, 1.75, 2, .75];
      player.querySelector('[data-speed]').addEventListener('click', event => {
        const speed = speeds[(speeds.indexOf(audio.playbackRate) + 1) % speeds.length];
        audio.playbackRate = speed;
        event.currentTarget.textContent = `${speed}×`;
        event.currentTarget.setAttribute('aria-label', text(`Playback speed: ${speed}×. Click to change`, `再生速度：${speed}倍。選択して変更`));
      });
      player.querySelectorAll('[data-enhanced]').forEach(element => { element.hidden = false; });
      player.classList.add('enhanced');
      status.textContent = '';
      updatePlay();
      update();
    } catch (error) {
      status.textContent = text('Interactive transcript unavailable. You can still listen, open the transcript, or listen on Spotify using the episode links.', '同期する文字起こしを読み込めません。音声の再生、全文を開くリンク、Spotifyは引き続きご利用いただけます。');
    }
  });
})();
