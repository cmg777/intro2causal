# Spotify publishing

This folder contains the configuration and publication records for **Mastering
Causal Metrics**. Publishing happens through an agent controlling Spotify for
Creators in the browser, only when requested in chat. No Spotify credentials,
cookies, tokens, paid host, or MCP server are required here.

## Prepare

From the repository root, run:

```sh
.venv/bin/python scripts/prepare_spotify.py --check-links
```

Requires Python 3.12+, Pillow, ffmpeg, and ffprobe (available in this project's
environment). The command validates square RGB artwork, decodes each entire MP3,
checks its hash and duration against alignment metadata, validates VTT cues and
the 5 MB limit, and checks public transcript content against the local TXT file.
It writes `manifest.json` without contacting Spotify or modifying publication
records. A failure produces no replacement manifest; do not use an older manifest
after a validation failure. Omit `--check-links` for offline asset checks only.

`project.json` is the source of the show identity, descriptions, file paths, and
episode numbering. Paths are relative to the repository root. `state.json` holds
observed Spotify identifiers, status, URLs, and uploaded hashes. `review.md` is the
human-readable publishing package. Generated manifests contain absolute local
paths and remain ignored by Git.

## Agent publishing procedure

1. Read this guide, the current configuration, and state. Run preparation with
   public-link checks. Confirm that the requested episodes and destination match
   the user's request. Review the prepared artwork and copy with the user before
   the first upload. Do not treat review preparation as publication approval.
2. Use the browser UI to inspect the account and its shows. If `show_id` is null,
   look for the configured title before creating a new Spotify-hosted show.
   Record the observed ID and public URL immediately after creation. Select
   English, Courses (under Education where offered), and non-explicit content.
   If Spotify presents new legal terms, ask for action-time confirmation before
   accepting them. Never change another show's settings.
3. Inspect the target show's existing episodes, including drafts, before any
   upload. Match episode title/number to state and resolve uncertainty before
   retrying. A state record alone does not prove that a remote episode exists.
   Skip published episodes with unchanged hashes. Changed published assets cause
   preparation to fail: replacement requires a separate explicit request.
4. Upload the exact MP3 path in the manifest. Enter its title, description,
   episode number, full-episode type, and non-explicit setting. Use the episode's
   configured `artwork` if present, otherwise the show artwork. For existing
   episodes, `inspect_artwork_update` means update only the art after confirming
   the requested change; do not re-upload audio or republish. Record the saved
   `artwork_sha256` after observing success. Record the draft ID, URL, both file hashes, and status as
   soon as Spotify creates a draft. Do not store secrets or private account data.
5. Inspect transcript eligibility on this new show and each episode. Upload the
   matching VTT if supported. Keep automatic transcripts from replacing a custom
   upload. Record `transcript_mode` as `uploaded_vtt` only after observing success;
   otherwise use `linked_txt` with the reason. Always retain the description link.
6. Publish Chapter 1 first under the user's release authorization. Verify its
   public page, title, number, description links, beginning/middle/end playback,
   and the supplied transcript's display and approximate alignment if available.
   Do not report audio as verified from an upload-success message alone. If the
   browser cannot expose playback controls or sound verification, report that
   exact limitation and hold the remaining episodes for the pilot check.
7. After the pilot passes, publish Chapters 2–6 in ascending order. Verify each
   public page and playable audio, then record status `published`, its public URL,
   publication time, and verification results. Do not fabricate an ID or URL.
8. On interruption, inspect the saved draft before resuming. Record observed
   partial progress and the blocking reason. Preserve the browser page when
   handing off a login, CAPTCHA, legal confirmation, or unresolved upload.
9. Deliver the show URL, episode URLs, transcript mode, and any verification
   limitations. Save a screenshot of the published result for the user.

Future requests can say: “Publish Chapter 7 of Mastering Causal Metrics” or
“Prepare these episodes as drafts.” New episodes need matching audio, alignment
JSON, VTT, and publicly accessible TXT before publishing. The website deployment
is a separate action; never substitute a local URL for a public transcript link.

## Publication state

Keep the existing top-level project identifier. Add observed fields as work
progresses; an episode record has this shape (illustrative values only):

```json
{
  "spotify_id": "observed-episode-id",
  "creator_url": "https://creators.spotify.com/...",
  "url": "https://open.spotify.com/episode/...",
  "status": "draft",
  "audio_sha256": "hash-from-current-manifest",
  "transcript_sha256": "hash-from-current-manifest",
  "transcript_mode": "linked_txt",
  "transcript_note": "Observed eligibility limitation",
  "verified": {"public_page": false, "playback": false, "transcript_link": false}
}
```

Save records atomically after each observed change. Before publishing on a later
chat request, reconcile these records with Spotify's live episode list.

## Other projects

Copy `project.json` into the other project's `publishing/spotify/` folder and
replace its show identity, descriptions, links, and episode entries. Give it a
distinct `project_id` and initialize its own state with null show identifiers and
an empty episodes object. Never copy this show's Spotify IDs into another project.
The default repository root is two directories above the configuration; set
`root` relative to the configuration directory for another layout. Run the same
preparation script with `--config /path/to/project.json`; state and manifest
default to the configuration's directory. The script is standalone apart from
Pillow and ffmpeg, and can be copied with the configuration.

## Current status

All six episodes are published in [Mastering Causal Metrics](https://open.spotify.com/show/4eleEMEYrSr7pFwOeMuI0r). Spotify explicitly reports that native transcripts are unavailable for this podcast; every episode description links to its matching TXT transcript. See `state.json` for episode URLs, file hashes, and verification results.
The user's selected release sequence is Chapter 1, verify, then Chapters 2–6.
No unattended publishing or other podcast-platform submissions are enabled.

## Published episodes

| Episode | Spotify | Transcript |
|---|---|---|
| Chapter 1: Randomized Trials | [Listen](https://open.spotify.com/episode/3O60EvgThQMkkdb9Y3qonF) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch01-randomized-trials.txt) |
| Chapter 2: Regression | [Listen](https://open.spotify.com/episode/2gE66Q3fTts4fnU19mctyo) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch02-regression.txt) |
| Chapter 3: Instrumental Variables | [Listen](https://open.spotify.com/episode/2VnEMA9PTdX9x1zRnl0h56) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch03-instrumental-variables.txt) |
| Chapter 4: Regression Discontinuity | [Listen](https://open.spotify.com/episode/39cBXhzM2tEQ6Iy0IPHAxP) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch04-regression-discontinuity.txt) |
| Chapter 5: Differences-in-Differences | [Listen](https://open.spotify.com/episode/097YUmXOFyuwCr6xKKPyyB) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch05-differences-in-differences.txt) |
| Chapter 6: The Wages of Schooling | [Listen](https://open.spotify.com/episode/7Ai11CxTsj9yoVtL68UcvV) | [Read](https://cmg777.github.io/intro2causal/mindmaps-podcast/transcripts/ch06-wages-of-schooling.txt) |

Episode-specific square mind maps are stored in `episode-art/`. Each episode
configuration selects its matching map. These simplified Spotify designs were
generated separately from the widescreen book and website mind maps.
