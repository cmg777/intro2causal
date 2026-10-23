# Read-along transcripts for Chapters 1–6

The website uses each chapter's JSON file for passage highlighting and section
markers in the shared podcast player. “Open Transcript” opens a formatted HTML
reading page in a new tab while audio continues in the original tab. “Read along”
keeps the timed transcript inside the player. Text comes from the existing HOST/ECONOMIST script. Paragraph timings
are aligned to offline whisper.cpp recognition; they are approximate rather than
word-level timestamps. Section boundaries come from the original audio chunk
durations, including the assembler's inserted silences.

No API calls are needed to transcribe, build, or use the player. Recognition runs
on the local computer. A small English Whisper model is sufficient for alignment
because the script supplies the displayed text. The builder checks recognition
coverage for each chunk and turn, monotonic timestamps, and cache/audio duration
agreement before writing the three website assets.

To rebuild with the original matching PCM chunk cache still available:

```sh
ffmpeg -i mindmaps-podcast/audio/ch01-randomized-trials.mp3 -ar 16000 -ac 1 /tmp/ch01.wav
whisper-cli -m /path/to/ggml-tiny.en.bin -f /tmp/ch01.wav -l en -bs 1 -bo 1 -oj -of /tmp/ch01
python3 scripts/build_podcast_transcript.py \
  --recognition /tmp/ch01.json \
  --script mindmaps-podcast/ch01-randomized-trials.md \
  --audio mindmaps-podcast/audio/ch01-randomized-trials.mp3 \
  --cache .work/podcast/ch01-randomized-trials
```

Keep model files, raw recognition output, and PCM caches outside version control.
All six completed recordings (Opus and MP3 fallbacks) have specific exceptions
in `.gitignore` so GitHub Pages can serve them with their transcripts. Generation and verification caches stay local.

## Web audio delivery

Each player prefers 48 kbps variable-bitrate mono Opus, with the existing MP3 as a
browser fallback. Opus is encoded directly from the local lossless `episode.wav`
masters, avoiding a second lossy encode of the MP3. Both formats preserve episode
timing. Transcript JSON records the Opus size, duration and hash alongside the
original MP3 hash. Audio files load only when a listener interacts with playback.

To regenerate the compressed recordings and their metadata after rebuilding transcripts:

```sh
python3 scripts/compress_podcast_audio.py
```

The website offers transcript reading pages rather than download buttons. Existing
TXT, JSON, and VTT URLs remain available for compatibility. Native audio controls
request `nodownload` where supported. Public browser playback
still transfers audio and cannot prevent listeners from saving the underlying files.

## Transcript reading pages

After changing or rebuilding transcript JSON, regenerate all six committed HTML
reading pages with the standard-library-only command:

```sh
python3 scripts/build_transcript_pages.py
```

Pages use the JSON section boundaries, speaker labels, timestamps, and full text.
They remain readable without JavaScript; the optional theme toggle shares the
main site’s saved theme preference. No transcription or audio generation is needed.
Each player also links directly to its chapter’s published Spotify episode, using
the episode URLs recorded in `publishing/spotify/state.json`.
