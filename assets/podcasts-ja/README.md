# Japanese podcast collection images

The website uses the full Japanese chapter maps under `full/`. See
`full/README.md` and `mindmaps/ja/manifest.json` for provenance, approved
versions, generation prompts, reviews and native-resolution information.
The original square WebPs in this directory are legacy copies of the compact
Spotify artwork. They are not referenced by the Japanese podcast page.

The page uses the existing MP3 recordings for Chapters 1–5. Chapters 1–4 use
reviewed timed JSON and static reading pages under
`mindmaps-podcast/ja/transcripts/`, plus verified chapter-specific public
Spotify URLs. Chapter 5 has native playback until its transcript is ready.
Chapter 6 has a full Japanese mind map and a preparation notice.

When remaining audio/transcripts are ready, update chapter markup and the hero
availability summary. Preserve genuine transcript timestamps. Reuse the player
and change all chapter-specific IDs, media/transcript paths and verified
Spotify episode URLs. Run `scripts/test_japanese_podcasts_page.py`, updating
availability checks when a chapter is completed.
