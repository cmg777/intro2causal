# Podcast companions to the causal inference mind maps

One English HOST/ECONOMIST dialogue per chapter, for students new to econometrics.
Length follows the material; estimates below assume 150 spoken words per minute.
Generated on 2026-10-22 from this repository's files: 6 of 6 scripts written.

Audio recordings are available for 6 of 6 chapters. The table links to each existing recording; optional Audio Overview prompts are separate.
Use `/write-podcast-script4mindmaps 1` (or `chapters`) to write episodes.
Use `/write-podcast-script4mindmaps audit 1` to review an existing script and fix audit findings.
The skill's `reference/episode.md` defines the format and `reference/audit.md` defines the quality gate.
Lint and independent audit are separate checks; a missing or stale audit is not a pass.

Audio is optional and generated only when requested, after current lint and audit pass:

```bash
uv run --with 'google-genai>=2.25.0' python -I .claude/skills/write-podcast-script4mindmaps/scripts/pod_audio.py 1 --transcribe
```

See `reference/audio.md` in the skill for credentials, ffmpeg, optional local Whisper and model settings.
Prompt files provide an optional Audio Overview alternative; they are not uploaded as sources.
Website integration is deferred. Audio and caches are ignored by git; this skill does not commit or push.

| Chapter | Script | Prompt | Spoken words | Estimated minutes | Lint | Audit | Audio |
|---|---|---|---|---|---|---|---|
| Chapter 1 | [Script](ch01-randomized-trials.md) | — | 5278 | 35.2 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch01-randomized-trials.mp3) (38.9 min) |
| Chapter 2 | [Script](ch02-regression.md) | — | 5430 | 36.2 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch02-regression.mp3) (39.5 min) |
| Chapter 3 | [Script](ch03-instrumental-variables.md) | — | 4848 | 32.3 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch03-instrumental-variables.mp3) (35.4 min) |
| Chapter 4 | [Script](ch04-regression-discontinuity.md) | — | 4877 | 32.5 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch04-regression-discontinuity.mp3) (35.2 min) |
| Chapter 5 | [Script](ch05-differences-in-differences.md) | — | 4382 | 29.2 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch05-differences-in-differences.mp3) (31.9 min) |
| Chapter 6 | [Script](ch06-wages-of-schooling.md) | — | 6168 | 41.1 | PASS | PASS (min 5, mean 5.0) | [MP3](audio/ch06-wages-of-schooling.mp3) (45.6 min) |

## Source checks and reviews

The original book is the authority. Where a map or companion source differs, the scripts use the verified result and preserve the discrepancy in source notes. Original source files remain local and ignored.

- Chapter 1: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch01-randomized-trials/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch01-randomized-trials/audit.md)
- Chapter 2: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch02-regression/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch02-regression/audit.md)
- Chapter 3: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch03-instrumental-variables/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch03-instrumental-variables/audit.md)
- Chapter 4: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch04-regression-discontinuity/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch04-regression-discontinuity/audit.md)
- Chapter 5: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch05-differences-in-differences/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch05-differences-in-differences/audit.md)
- Chapter 6: [Source notes](../.claude/skills/write-podcast-script4mindmaps/state/ch06-wages-of-schooling/source-notes.md) · [Independent review](../.claude/skills/write-podcast-script4mindmaps/state/ch06-wages-of-schooling/audit.md)
