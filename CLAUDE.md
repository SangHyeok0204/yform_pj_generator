# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A generator for **Y-PJ-FoRM academic-society** PowerPoint decks (16:9, 13.33" × 7.5", Pretendard typography). Output is `.pptx` authored with `python-pptx` + `lxml`. Layout is rigidly anchored — every standard slide places the section title, hairline rule, subtitle, and body region at fixed coordinates, and the cover and TOC slides must visually match `reference/master_deck.pptx` pages 1 and 2 exactly.

## Sources of truth

- **`prompts/design_system.md`** — canonical layout/typography spec. All anchor coordinates, font weights, colors, density rules, and per-slide-type rules live here. **Treat this file as authoritative; if code diverges from it, the code is wrong.**
- **`reference/master_deck.pptx`** — visual ground truth. The cover slide is a verbatim reproduction of its page 1 (only the project-title text is swapped); the TOC is a verbatim reproduction of its page 2.
- **`reference/cover_reference.png`** — pre-rendered cover (1920×1080) used as a final cross-check; never insert it as a flat background, layer the components instead.
- **`reference/past_outputs/`** — earlier generated decks (`Y-PJ-FoRM_Basis_Trading*.pptx`, `..._KOSPI200_DeltaHedging.pptx`); useful for diffing but not authoritative — some predate the current spec.

## Implementation

The PPTX builder lives in **`api/_lib/engine.py`** — a content-agnostic renderer. Public entry `render_deck(content: DeckContent) -> bytes` consumes a `DeckContent` Pydantic model (defined in `api/_lib/schema.py`) and emits PPTX bytes. The intended pipeline: an LLM produces structured `DeckContent` JSON from source material → engine renders it. The block grammar (`h`, `p`, `li`, `gap`, `caption`) in `schema.py` mirrors the structural composition rules in `design_system.md`.

The original standalone script `build_deck.py` was extracted into the engine and is preserved at **`scripts/_legacy_build_deck.py`** for reference only. Byte-identical regeneration was verified against `reference/past_outputs/Y-PJ-FoRM_KOSPI200_DeltaHedging.pptx` (20,071,258 bytes). Do not edit the legacy script; layout changes go in `engine.py`.

Helpers in `engine.py`: `add_textbox`, `style_run`, `add_hairline`, `add_section_title`, `add_subtitle`, `add_body_paragraphs`. Slide builders: `build_cover`, `build_toc`, `build_content`.

## Running

```bash
# Render the bundled KOSPI 200 example through the engine (writes reference/past_outputs/...__regen.pptx)
python scripts/render_local.py

# Re-extract content from the legacy script to JSON (one-shot; rarely needed)
python scripts/extract_kospi200_to_json.py

# Frontend (after `npm install`)
npm run dev      # local Next.js at http://localhost:3000
npm run build    # production build
```

Python dependencies are pinned in `requirements.txt` (`anthropic`, `python-pptx`, `lxml`, `pydantic`, `python-docx`, `pymupdf`). Frontend dependencies in `package.json` (Next.js 15 + React 19 + Tailwind v4). `vercel.json` configures the Python function (`maxDuration: 800`, asset excludes).

## Asset and font layout

- `assets/images/` — `cover_hero_main.png`, `cover_hero_strip.png`, `logo.jpg`, `toc_decor.png`. The engine reads these via `PROJECT_ROOT / "assets" / "images"`.
- `public/fonts/` — the nine Pretendard `.OTF` files (Thin → Black). Used for *local installation*; the generators reference fonts **by name** (`Pretendard ExtraLight / SemiBold / ExtraBold`) and rely on the author's machine having Pretendard installed. Final font embedding into the `.pptx` is delegated to PowerPoint's native `File → Options → Save → Embed fonts in the file` toggle — the pipeline never injects font binaries.
- `samples/` — source `.docx` / `.pdf` documents for paper content (input fodder for the LLM stage).
- `app/` — Next.js App Router (`layout.tsx`, `page.tsx`, `globals.css`). Currently a placeholder upload page; the API integration lives in `api/`.
- `components/`, `lib/` — Frontend React components and TS utilities (currently empty scaffolds; populate as features land).
- `prompts/examples/` — Few-shot `DeckContent` JSON for the LLM. Ground truth: `kospi200_delta_hedging.json` extracted byte-identically from the original deck.
- `api/_lib/extract/` — Reserved for `.docx` / `.pdf` text extractors (not yet implemented).
- `scripts/`, `tests/` — Local-only (excluded from Vercel function bundle by `vercel.json`).

## Spec-critical invariants (the things people get wrong)

Before editing any `build_toc` or `build_cover`, read `prompts/design_system.md`'s *Cover Anchors* and *TOC Anchors* sections. These rules have caused the most regressions:

1. **No `logo.jpg` outside the cover.** The TOC's right strip is filled by `toc_decor.png` at `(X=10.12", Y=-0.04", W=11.29", H=7.50")` — intentionally oversized so it overflows the canvas right edge. Never substitute the logo here.
2. **`Contents` header is Pretendard SemiBold 50pt** (weight 600), not ExtraBold. ExtraBold 800 is reserved for the cover display title.
3. **TOC list is a single textbox** holding one paragraph per section in the form `N. Section Name`, Pretendard ExtraLight 20pt, navy. One run per paragraph — do **not** split numerals into separate red runs, do **not** lay out as two columns, do **not** add per-item subtitles.
4. **No red anywhere.** The active palette is black, navy `#122B46`, and white. Society red `#C00000` is forbidden on every slide type — the prior "TOC numerals may be red" allowance was removed because the reference deck contains zero red.
5. **No page numbers, no footer slugs** (`Y-PJ-FoRM 39th` etc.) on any slide, including the TOC.
6. **TOC has two hairline rules** — the short top rule (`Y=1.20"`, X 0→10.12") and the full-width bottom rule (`Y=6.70"`, X 0→13.33"). Both mandatory.
7. **Standard slides have the hairline at `Y=0.93"` full-width.** Non-negotiable; never shift the master anchors to "balance" a slide.

## Known code/spec drift to be aware of

`api/_lib/engine.py:build_toc()` still emits the **legacy** TOC (uses `F_BOLD`/ExtraBold for `Contents`, `RED` for `01.` numerals, omits `toc_decor.png`). This was preserved during the engine extraction so byte-identical regression checks against `reference/past_outputs/` would pass. The spec in `prompts/design_system.md` is authoritative and the TOC builder still needs to be aligned with it (SemiBold 50pt, no red, `toc_decor.png` strip). Track this as the next layout-correctness task before launching the web flow.

The legacy `scripts/_legacy_build_deck.py` references assets via `os.path.join(ROOT, 'cover_hero_main.png')`, which is stale (assets now live under `assets/images/`). Do not run it; the engine uses the correct `ASSETS_DIR` constant.

## Slash commands (`.claude/commands/`)

- `/start` — restore project context at session start; responds in Korean by directive.
- `/check`, `/dev` — TS/lint/test stubs (not applicable to this Python project; ignore unless wiring up tooling).
- `/learned`, `/refactoring` — generic agent prompts.
