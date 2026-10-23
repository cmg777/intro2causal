# Japanese podcast collection images

These are 1000 × 1000 WebP display copies (quality 88) of the accepted Japanese
mind maps in `publishing/spotify-jpn/artwork/chNN-*.png`. No content was changed.
The full-size links on `podcasts-ja.html` open those original PNG exports.

The page currently uses the existing MP3 recordings for Chapters 1–5. Chapters
1–4 use the reviewed timed JSON and static reading pages under
`mindmaps-podcast/ja/transcripts/`, plus the chapter-specific public Spotify URLs
in `publishing/spotify-jpn/state.json`. Chapter 5 has native playback only until
its transcript is ready. Chapter 6 has a mind map and a preparation notice.

When the remaining materials are ready, update each chapter's markup and the
availability summary in the hero. Preserve transcript timestamps; do not derive
timing from the script. Reuse the established player markup and change every
chapter-specific ID, audio/transcript path and verified Spotify episode URL.
Run `scripts/test_japanese_podcasts_page.py`, updating its availability checks
when a chapter is completed.
