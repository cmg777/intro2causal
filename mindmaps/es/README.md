# Spanish chapter mind maps

Faithful Spanish (neutral Latin American, *tú*) translations of the six full English chapter maps
(`book/images/chNN_visual_summary.webp`), shown on the Spanish home page `index-es.html`.

- `images/` — approved native PNGs (1672 × 941, the size the generator returned; no upscaling).
- `prompts/` — `_common.txt` plus each chapter's exact Spanish text. `*-fix.txt` prompts are the targeted
  correction passes that produced v2/v3 (spelling and a missing label); the drafts they replaced were deleted.
- `manifest.json` — selected versions, source and output hashes, dimensions and review notes.

Generated with the Codex CLI built-in image tool. Each image was reviewed manually against its English
source: every branch, bullet, label, equation, number and arrow direction. Diagrams are schematics, not
new results. Re-export the web copies with `uv run python scripts/export_spanish_mindmaps.py`.
