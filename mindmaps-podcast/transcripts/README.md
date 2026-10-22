# Read-along transcripts for Chapters 1–6

The website uses each chapter's JSON file for passage highlighting and section
markers in the shared podcast player. Students can download the plain-text (`.txt`) or timed WebVTT (`.vtt`)
versions. Text comes from the existing HOST/ECONOMIST script. Paragraph timings
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
All six completed MP3s have specific exceptions in `.gitignore` so GitHub Pages
can serve them with their transcripts. Generation and verification caches stay local.
