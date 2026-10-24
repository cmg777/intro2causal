# Full Japanese chapter mind maps

Japanese translations of the six full English chapter maps in
`book/images/chNN_visual_summary.webp`, for `podcasts-ja.html`.

The user approved Chapter 1 version 2's larger Japanese Gothic-style lettering,
white-on-dark-navy contrast, complete content and English technical headings.
Chapters 2–6 apply that direction. These are separate from Spotify cover art.

## Selected assets and provenance

`manifest.json` identifies the six selected PNGs and optimized WebPs, exact
prompts, English source hashes, output hashes, native dimensions and manual
content/diagram checks. `images/` holds the native full-size PNGs. `prompts/`
holds the exact translated copy and imagegen requests. `review/` records the
checks; chapter Markdown files describe translation choices and caveats.

Built-in `image_gen.imagegen` generated all images. Generated lettering follows
Noto Sans JP / BIZ UDPGothic stylistic instructions but is not an embedded or
verified font. Native outputs are 1672 × 941; 3840 × 2160 was requested but not
returned. No images were upscaled. PNG→WebP encoding preserves all content.

## Accuracy and interpretation

Each full English map, not its abbreviated Spotify counterpart, is the content
and composition reference. Read `mindmaps/audit/econometric-audit.txt` for the
English maps' assumptions, mathematical identities, source checks and scope.
Selected numerical findings match the local notebooks and the numerical audit.
Reported literature summaries without microdata remain approximate summaries,
not newly calculated estimates. Source conceptual graphics retain their
mathematical geometry; Chapter 6's artificial-data illustrations retain labels.

Chapter 1 version 1 and its original prompts/review are historical comparisons.
The current site uses Chapter 1 version 2 and Chapters 2–6 version 1.

## Website verification

Run `scripts/test_japanese_podcasts_page.py` with Playwright to check all six
chapter mappings, hashes, landscape geometry, full-size links and existing
playback/transcript behavior. The geometry record in `review/geometry-checks.json`
adds pixel checks for the DD diagrams' parallel pre-treatment lines. These
checks support manual review; they are not OCR or evidence for causal validity.
