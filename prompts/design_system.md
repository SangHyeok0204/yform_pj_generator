# Design System Prompt — Y-PJ-FoRM Academic Society Deck (Pretendard / PPTX)

> **Use:** This document is a design-system prompt for Claude to author PowerPoint (`.pptx`) presentations for the Y-PJ-FoRM academic society. It encodes the visual language defined by the reference template `Y-PJ-FoRM-2026.pptx` and is expressed entirely in **Pretendard**. Output format is **`.pptx`** authored via `python-pptx` (or equivalent), with all coordinates given in inches for direct application.

## Required Project Attachments (filenames are exact — do not rename)

> When this prompt is used inside a Claude.ai Project, the following files **must** be attached to the project. Claude refers to them by the **exact filenames** below. If a file is missing, halt and ask the user to attach it before generating the deck.

| Filename | Purpose | How Claude must use it |
|---|---|---|
| `Y-PJ-FoRM-2026.pptx` | Original reference deck. | Read-only reference for layout, anchors, and the cover composition. Never link to it from the generated deck. |
| `cover_reference.png` | Pre-rendered image of slide 1 of `Y-PJ-FoRM-2026.pptx` (1920×1080). | **Visual cross-check only.** After authoring the cover, the layered output must look identical to this image. **Do not** insert `cover_reference.png` as a flat background — the cover title must remain editable text. |
| `cover_hero_main.png` | Main cover photograph (skyscraper composition). | Insert on the cover slide at (X = 0.00", Y = 0.00", W = 10.09", H = 6.70"). |
| `cover_hero_strip.png` | Bottom-right cover strip (complementary crop). | Insert on the cover slide at (X = 10.09", Y = 6.70", W = 3.24", H = 0.80"). |
| `logo.jpg` | Y-FoRM identity mark. | Insert on the **cover slide only** at (X = 10.58", Y = 1.14", W = 2.27", H = 1.70") per *Cover Anchors*. Never place this file on any other slide — the TOC's right strip is filled by `toc_decor.png`, never the logo. |
| `toc_decor.png` | Decorative right-side graphic used on the **TOC slide** in `Y-PJ-FoRM-2026.pptx` slide 2. | Insert on the **TOC slide** at (X = 10.12", Y = -0.04", W = 11.29", H = 7.50"). The image is intentionally oversized — only the leftmost ~3.21" (from X = 10.12" to the canvas right edge X = 13.33") is visible; the remainder runs off-canvas. Insert at the listed full size. **Do not crop, scale, or substitute.** **Mandatory** on every TOC slide. |
| `PRETENDARD-EXTRALIGHT_0.OTF` | Pretendard Weight 200. | Reference by name `Pretendard ExtraLight` for body and TOC items. |
| `PRETENDARD-SEMIBOLD.OTF` | Pretendard Weight 600. | Reference by name `Pretendard SemiBold` for section titles, subtitles, member roster. |
| `PRETENDARD-EXTRABOLD.OTF` | Pretendard Weight 800. | Reference by name `Pretendard ExtraBold` for the **cover display title** only. The TOC `Contents` header uses Pretendard **SemiBold** 50pt, not ExtraBold. |
| `PRETENDARD-THIN_0.OTF`, `PRETENDARD-LIGHT_0.OTF`, `PRETENDARD-REGULAR_0.OTF`, `PRETENDARD-MEDIUM.OTF`, `PRETENDARD-BOLD.OTF`, `PRETENDARD-BLACK.OTF` | Remaining Pretendard weights. | Available but not used in standard slides. Bold 700 may be used for inline strong emphasis inside body copy. |

**Filename discipline**: throughout this document, every backticked name like `cover_hero_main.png` refers to the **attached file with that exact filename**. Do not substitute, rename, or use a different image even if visually similar.

## Overview

The deck reads as an **editorial-academic document**: information-dense, typographically disciplined, and structurally repetitive so the audience can focus on substance rather than chrome. **The cover is a verbatim reproduction of slide 1 of `Y-PJ-FoRM-2026.pptx` — same imagery, same composition, same anchors — with only the project-title text swapped in.** Every other slide is anchored to a fixed grid:

1. **Section title** in the top-left (40pt SemiBold).
2. A **full-width hairline rule** immediately beneath the title at Y = 0.93".
3. A **subtitle / sub-section line** beneath the rule.
4. The **body region** (text, figures, tables) below the subtitle, pushed to the bottom safe edge.

Density is high and disciplined. The body region must be substantively populated to within ~0.3" of its bottom edge — empty lower halves are treated as defects, never as breathing room. Color is overwhelmingly white-on-white with a single restrained accent (deep navy `#122B46`); no red, no dark slides, no gradients, no decorative chrome.

**Key Characteristics**
- Cover slide is a 1:1 reproduction of `Y-PJ-FoRM-2026.pptx` slide 1 — only the project-title text is replaced. Reference render attached as `cover_reference.png`.
- Every non-cover slide carries a horizontal hairline rule at Y = 0.93" spanning the full 13.33" canvas width, immediately under the section title.
- Light surfaces only: pure white canvas (`#FFFFFF`); dark slide variants are explicitly forbidden.
- Three-rung typographic ladder: **Pretendard ExtraBold 800** (cover display) / **SemiBold 600** (section titles, subtitles, cover member line) / **ExtraLight 200** (body, TOC items).
- One accent color: deep navy `#122B46`. Society red `#C00000` is forbidden everywhere — the reference deck contains zero red.
- Section title, hairline rule, subtitle, and body region are anchored to identical coordinates on every standard content slide so the audience never re-locates the page furniture.
- Cover, TOC, and body slides are the only three primary surfaces. No dark divider, no full-bleed photo slide outside the cover, no closing flourish.
- Body density 60–80% — sparse residual is filled by **structured prose, sub-headings, and indented numbered/labeled lists first**, not by stacks of card containers. Cards, KPI tiles, callout chips, and reference cards are exception components, not the default scaffolding.
- **Palette is black + navy + white only on every slide, including the TOC.** No red anywhere in the deck.
- **No inline bold emphasis inside body paragraphs.** Bold (SemiBold/ExtraBold) is reserved for section titles, subtitles, and clearly labeled sub-section headings (e.g., `예시 —`, `메커니즘`, numbered tile labels). Mid-sentence emphasis like **bolded keywords** inside a running paragraph is forbidden — let the prose carry the meaning unaided.

## Colors

> Single light surface, two accents. No tints, no gradients, no parchment.

### Brand & Accent
- **Society Navy** (`{colors.primary}` — `#122B46`): Primary mark color. Used for section-title text, the hairline rule under section titles, callout chip backgrounds at 100%, KPI numerals. The deck's default "this is structural" cue.
- **Society Red** (`{colors.accent}` — `#C00000`): **Forbidden on every slide type in this deck system, including the TOC.** The reference deck `Y-PJ-FoRM-2026.pptx` contains zero red occurrences — TOC numerals are set in the same navy/black as the rest of the item, never in red. No red text, no red chips, no red numerals, no red rules on `slide-cover`, `slide-toc`, `slide-content`, `slide-data`, or `slide-quote`. The token is retained as a legacy name only; do not instantiate it.

### Surface
- **Pure White** (`{colors.canvas}` — `#FFFFFF`): The only canvas. Cover, TOC, content, and any future variant.
- **Hairline Gray** (`{colors.hairline}` — `#E0E0E0`): 1px borders on data table rows and inline reference cards.
- **Soft Divider** (`{colors.divider-soft}` — `#F0F0F0`): Faint separators inside multi-block content slides; functions as a ring rather than a hard line.

### Text
- **Ink** (`{colors.ink}` — `#000000`): Body text default. Used at all body sizes on white surfaces.
- **Ink Strong** (`{colors.ink-strong}` — `#122B46`): Section titles and cover display title (when navy emphasis is desired). Default to ink-strong (navy) for section titles — the reference template uses this rhythm.
- **Ink Muted** (`{colors.ink-muted}` — `#7A7A7A`): Captions, footnotes, and de-emphasized labels.

### Brand Gradient
**No decorative gradients.** Atmospheric depth on the cover hero photograph is inherent to the imagery, never a CSS or PPT gradient overlay. This deck system explicitly rejects gradient-based fills.

### Forbidden
- No dark surfaces (`{colors.surface-tile-*}` from the predecessor system are removed).
- No second accent beyond navy. Red is forbidden.
- No tints/transparencies of the brand colors except the two documented chip variants below.

## Typography

### Font Family
- **Display & Body**: `Pretendard` — a single typographic family carries the entire deck. All nine weights are available as embedded `.OTF` files in the project folder (`PRETENDARD-THIN.OTF` through `PRETENDARD-BLACK.OTF`).
- **No fallback typeface** is permitted in the rendered output. The author's environment is assumed to have Pretendard installed locally; the nine `PRETENDARD-*.OTF` files in the project attachments are provided for installation. Final embedding into the `.pptx` is delegated to PowerPoint's native option (`File → Options → Save → Embed fonts in the file`); the generation pipeline does not inject font binaries.

### Available Weights (uploaded font files in project root)

| Pretendard Weight | Numeric | File |
|---|---|---|
| Thin | 100 | `PRETENDARD-THIN_0.OTF` |
| ExtraLight | 200 | `PRETENDARD-EXTRALIGHT_0.OTF` |
| Light | 300 | `PRETENDARD-LIGHT_0.OTF` |
| Regular | 400 | `PRETENDARD-REGULAR_0.OTF` |
| Medium | 500 | `PRETENDARD-MEDIUM.OTF` |
| SemiBold | 600 | `PRETENDARD-SEMIBOLD.OTF` |
| Bold | 700 | `PRETENDARD-BOLD.OTF` |
| ExtraBold | 800 | `PRETENDARD-EXTRABOLD.OTF` |
| Black | 900 | `PRETENDARD-BLACK.OTF` |

**Active ladder for this deck**: **200 / 600 / 800**. All other weights are present in the file set but are not used in standard slides. Bold 700 may be used inside body copy for inline strong emphasis, sparingly. Weights 100 / 300 / 400 / 500 / 900 are reserved and should not appear in any rendered slide unless an explicit exception is documented.

### Hierarchy

> Sizes are expressed in **pt** (PowerPoint native). Slide canvas is 16:9, 13.33" × 7.5".

| Token | pt | Weight | Tracking | Use |
|---|---|---|---|---|
| `{type.cover-display}` | 40pt | 800 (ExtraBold) | -2% | Cover slide project title (English). The signature ExtraBold display. Replaces the placeholder text `플젝명 (영어로) 작성` in `Y-PJ-FoRM-2026.pptx` slide 1. |
| `{type.cover-member}` | 20pt | 600 (SemiBold) | 0 | Cover bottom-strip member roster — `{name} {cohort}th, {name} {cohort}th, …` |
| `{type.toc-header}` | 50pt | **600 (SemiBold)** | -2% | The `Contents` header on the TOC slide. Set in `{colors.ink-strong}` navy (or theme text color). **The reference deck `Y-PJ-FoRM-2026.pptx` slide 2 uses SemiBold 600 here, NOT ExtraBold 800.** Bold flag may be enabled on the run, but the underlying weight is SemiBold. |
| `{type.toc-item}` | 20pt | 200 (ExtraLight) | 0 | Numbered TOC items. **One paragraph per item**, formatted as `N. Section Name`; numeral and section name share a single run. Set in `{colors.ink-strong}` navy (or theme text color). **Never split the numeral into a separate red run** — red is forbidden on the TOC. |
| `{type.section-title}` | 40pt | 600 (SemiBold) | -1% | The per-slide H1 anchor on every standard content slide. Format: `N. Section Name`. Set in `{colors.ink-strong}` navy. |
| `{type.section-subtitle}` | 24pt | 600 (SemiBold) | 0 | The per-slide H2 line below the hairline rule. Optional but expected on most slides. Format: `N.M Sub-section Name` or a short descriptive phrase. Set in `{colors.ink}` or `{colors.ink-strong}`. |
| `{type.body}` | 20pt | 200 (ExtraLight) | 0 | Default body paragraph. May shrink to 18pt or 16pt when content density requires it. |
| `{type.body-strong}` | 20pt | 600 (SemiBold) | 0 | Inline strong emphasis inside body copy; sub-headers within body sections. |
| `{type.kpi-numeral}` | 56pt | 800 (ExtraBold) | -3% | Large numeric callouts inside KPI tiles. Set in `{colors.ink-strong}` or `{colors.accent}`. |
| `{type.kpi-label}` | 14pt | 600 (SemiBold) | 0 | The label beneath a KPI numeral. Set in `{colors.ink-muted}`. |
| `{type.caption}` | 12pt | 400 (Regular) | 0 | Captions, footnotes, source attributions, image captions. |
| `{type.caption-strong}` | 12pt | 600 (SemiBold) | 0 | Emphasized captions; data table headers. |

### Principles

- **Three-weight discipline.** ExtraLight 200 is the body voice; SemiBold 600 is the structural voice; ExtraBold 800 is the cover voice. Mid-weights are an anti-pattern.
- **Body at 20pt, not 18pt or 16pt.** The reference template explicitly sets body copy at 20pt for legibility in academic settings. Shrinking is permitted only when content cannot be reduced further.
- **Korean line-break rules.** All text shapes must enable `{wordWrap}` and disable mid-word breaking. When authoring HTML or web preview, use `word-break: keep-all; overflow-wrap: break-word; line-break: strict;` so 어절 단위로 줄바꿈되고 조사("이/가/은/는/을/를/의")가 줄머리에 남지 않는다.
- **Numeric tabular alignment.** When a KPI grid or data column displays digits, enable Pretendard's `tnum` feature where the renderer supports it; otherwise size each digit cell to the same width.
- **Negative letter-spacing on display sizes only.** ExtraBold 40pt and 50pt headlines carry slight tracking tighten (-1% to -3%); body and caption sizes use neutral tracking. Never tighten below 16pt.
- **No secondary typeface.** Pretendard is the only typeface — display, body, captions, numerals, and any monospace data alike. If a code-block or monospace rendering is unavoidable, use Pretendard at weight 400 with the `tnum` feature; do not introduce a separate mono family.

### Pretendard Implementation Notes (PPTX)

- Pretendard must be installed on the authoring machine before opening the generated `.pptx`. The nine `.OTF` files in the project root cover all weights in this system.
- The final `.pptx` author enables PowerPoint's native font-embedding option (`File → Options → Save → Embed fonts in the file`, with "Embed only the characters used" recommended to keep file size down) so the deck renders identically on machines without Pretendard installed.
- Pretendard's Korean glyphs share the family namespace; mixed Korean/Latin slides do not require a fallback face.
- Set the slide master default text style to `Pretendard ExtraLight` so any text that escapes explicit styling still inherits the deck's base voice.

## Layout

### Slide Canvas
- **Aspect ratio:** 16:9, **13.33" × 7.5"** (= 1280pt × 720pt = 1920px × 1080px at 2× authoring).
- **Outer margin (safe area):** 0.20" on all sides at minimum; section title and body region snap to **0.12" left margin** as in the reference template (intentionally tight).
- **Live area:** approximately 13.09" × 7.30" after safe-area inset.
- **Column grid:** Implicit 12-column at ~1.10" wide each across the 13.09" content width. Body content may use the full 13.09" since no logo or page-number gutter intrudes anywhere on the canvas.
- **Vertical baseline:** 0.05" (~3.6pt). All text and image edges should snap to this baseline.

### Spacing System
- **Base unit:** 0.05" (~3.6pt) for typographic rhythm; structural layout snaps to 0.10" / 0.20" / 0.40" / 0.80".
- **Tokens:** `{spacing.xxs}` 0.05" · `{spacing.xs}` 0.10" · `{spacing.sm}` 0.20" · `{spacing.md}` 0.30" · `{spacing.lg}` 0.50" · `{spacing.xl}` 0.80" · `{spacing.section}` 1.20".
- **Card padding:** `{spacing.md}` 0.30" inside inline reference cards.

### Whitespace Philosophy
The top of every standard slide already provides breathing room above the section title (~0.09"). The body region (top edge ~Y = 1.62", bottom edge Y = 7.20") is **work area**, not air. No slide ever ends with a large empty bottom; see *Body Density Strategy*.

## Slide Layout Anchors

> The deck's most enforced rule on standard slides: **section title at top, hairline rule at Y = 0.93", subtitle below, body region beneath.** The cover overrides everything with its bespoke composition (a verbatim copy of `Y-PJ-FoRM-2026.pptx` slide 1).

### Master Anchors (16:9, 13.33" × 7.5", inches) — applies to every NON-COVER slide

| Element | X | Y | Width | Height | Notes / Token |
|---|---|---|---|---|---|
| **Section Title** (H1) | 0.12" | 0.09" | 13.09" | 0.77" | `{type.section-title}` Pretendard SemiBold 40pt, `{colors.ink-strong}` navy. Format: `N. Section Name`. Width is the full live area — no logo gutter is reserved on the right. |
| **Hairline Rule** (under title) | 0.00" | 0.93" | 13.33" | 0pt | Horizontal line spanning the entire slide width. Stroke 0.75pt, color `{colors.ink-strong}` `#122B46` navy (or `{colors.ink}` `#000000`). **Mandatory on every non-cover slide, including the TOC variant described below.** |
| **Section Subtitle** (H2) | 0.14" | 1.00" | 13.05" | 0.55" | `{type.section-subtitle}` Pretendard SemiBold 24pt. Format: `N.M Sub-section Name`, or omit entirely when not applicable. When omitted, the body region top edge moves up to Y = 1.05". |
| **Body Region** (top edge) | 0.12" | 1.62" | 13.09" | 5.58" | Body content starts here when a subtitle is present. When the subtitle is omitted, top edge shifts up to Y = 1.05" and height grows to 6.15". |
| **Body Region** (bottom edge) | 0.12" | 7.20" | 13.09" | — | End of live body area. Content must extend to within 0.30" of this edge. |

> **No top-right logo, no bottom-right page number, no footer slug.** The deck system explicitly removes all persistent corner marks. The full canvas — top-right corner included — is available for content. Do **not** introduce any "Y-PJ-FoRM Academic Society" mark, page count, project short-name, or watermark on standard slides.

### Cover Anchors (slide-cover only)

> The cover follows the layout of `Y-PJ-FoRM-2026.pptx` slide 1 with two adjustments codified below: (1) the project title is **constrained inside the hero photograph and left-aligned**, and (2) the society logo is **lowered into the white right-hand strip** (not bleeding above the top edge). The pre-rendered reference image attached as `cover_reference.png` (1920×1080) reflects these adjusted coordinates and is for visual confirmation only — do **not** flatten it into a single background image; layer the components below so the project-title text remains editable.

| Element | X | Y | Width | Height | Notes |
|---|---|---|---|---|---|
| **Hero Image (left/main)** | 0.00" | 0.00" | 10.09" | 6.70" | Full hero photograph (skyscraper composition), top-left bleed. Insert the attached file `cover_hero_main.png`. Identical to the reference. |
| **Hero Strip (bottom-right)** | 10.09" | 6.70" | 3.24" | 0.80" | Complementary crop of the same hero composition. Insert the attached file `cover_hero_strip.png`. Fills the bottom-right corner. |
| **Society Logo (cover only)** | 10.58" | 1.14" | 2.27" | 1.70" | The Y-FoRM identity mark, fully visible in the upper portion of the white right-hand strip. Insert the attached file `logo.jpg`. **This logo is part of the cover composition only — it does NOT appear on any other slide.** |
| **Project Title** | 0.50" | 2.91" | 9.20" | 2.42" | `{type.cover-display}` Pretendard ExtraBold 40pt. **Left-aligned**, vertical-center within the box. The text box must fit **entirely inside the hero photograph** (right edge ≤ 9.70" so the title never extends into the white right-hand strip). Set in `{colors.canvas}` white when the hero composition is dark (the default skyscraper image), or `{colors.ink-strong}` navy when the hero composition is light. May wrap to two lines. **This is the only string the author edits on the cover.** |
| **Member Roster** | 0.20" | 6.88" | 9.41" | 0.44" | `{type.cover-member}` Pretendard SemiBold 20pt. Format: `Y-FoRM {cohort}th {name}, {cohort}th {name}, …`. Left-aligned. Sits on the white strip beneath the main hero. |

The cover reference image is the attached file `cover_reference.png` — view it for visual confirmation before generating the deck. Do not deviate from this composition.

### TOC Anchors (slide-toc only)

> The TOC is a **verbatim reproduction of `Y-PJ-FoRM-2026.pptx` slide 2.** Every element below is mandatory; nothing on this slide is optional. The Y-FoRM logo (`logo.jpg`) **must NOT appear** on this slide (or any non-cover slide). All coordinates were derived directly from the reference deck and must be applied exactly.

| Element | X | Y | Width | Height | Notes |
|---|---|---|---|---|---|
| **TOC Decorative Picture** | 10.12" | -0.04" | 11.29" | 7.50" | Insert the attached file `toc_decor.png`. The image is intentionally oversized — only the leftmost ~3.21" is visible (from X = 10.12" to the canvas right edge X = 13.33"); the remainder runs off-canvas. **Insert at the full listed size — do NOT crop, scale, or resize the image.** This is the right-side decorative strip. **Mandatory.** |
| **`Contents` Header** | 0.31" | 0.11" | 4.51" | 0.94" | `{type.toc-header}` **Pretendard SemiBold 50pt** (weight 600, not 800). The literal English word `Contents`. Set in `{colors.ink-strong}` navy or theme text color. Bold flag may be enabled, but the underlying weight remains SemiBold. **Do NOT use ExtraBold 800 here** — that weight is reserved for the cover display title. |
| **Hairline Rule** (under header) | 0.00" | 1.20" | 10.12" | 0pt | Short horizontal line — **TOC variant** of the hairline (10.12" wide, not full canvas, mirroring the reference deck). Stroke 0.75pt, `{colors.ink-strong}` navy. **Mandatory.** |
| **Numbered List** | 0.31" | 1.34" | 9.45" | 3.13" | A **single text box** containing one paragraph per TOC item, formatted as `N. Section Name` (e.g., `1. Overview`, `2. Theta, Gamma, Vega, Rho`). Numeral and section name share **one run** in `{type.toc-item}` Pretendard ExtraLight 20pt, set in `{colors.ink-strong}` navy or theme text color. **Single column, left-aligned, no per-item subtitle, no per-item chip, no two-column split, no red.** List order need not mirror any textbook. |
| **Bottom Rule** | 0.00" | 6.70" | 13.33" | 0pt | Full-canvas-width horizontal line at the lower edge. Stroke 0.75pt, `{colors.ink-strong}` navy. **Mandatory** — present in the reference deck on every TOC. |

**Forbidden on the TOC slide (explicit list — these caused defects in earlier generations):**
- The Y-FoRM logo (`logo.jpg`). The logo lives on the cover slide only; the TOC's right strip is filled by `toc_decor.png`, not the logo.
- Per-item red numeral chips (`01`, `02`, …) or any red coloring on numerals.
- A two-column TOC layout that splits items into a left/right grid.
- Per-item subtitle / sub-description lines beneath the section names.
- Splitting numeral and title into separate runs or text boxes.
- A bottom-left `Y-PJ-FoRM Nth` footer slug or a bottom-right page number.

### Anchor Discipline Rules
- **Cover is verbatim.** The cover composition is `Y-PJ-FoRM-2026.pptx` slide 1 reproduced exactly. Only the project-title text changes. No other element on the cover may be moved, resized, recolored, replaced, or removed.
- **TOC is verbatim.** Likewise, the TOC composition is `Y-PJ-FoRM-2026.pptx` slide 2 reproduced exactly — five layered elements (`toc_decor.png` right strip, `Contents` SemiBold header, short top rule, single-textbox numbered list in ExtraLight, full-width bottom rule), and only the section names inside the list are edited per project.
- **Hairline rule is non-negotiable on non-cover slides.** Every non-cover slide carries the full-width hairline at Y = 0.93". The TOC replaces this with **two** rules: the short top variant at Y = 1.20" (X = 0 to 10.12") and the full-width bottom rule at Y = 6.70" (X = 0 to 13.33"). Both TOC rules are mandatory.
- **Section title may wrap to two lines.** When the title wraps, the hairline rule does **not** move; instead the section title shrinks to fit on one line (or the title is rewritten more concisely). The Y = 0.93" anchor for the hairline is a hard floor.
- **No logos or marks on non-cover slides.** Do not place the Y-FoRM logo (`logo.jpg`), an "Academic Society" mark, a page number, or a project short-name on any slide other than the cover. The corner zones are pure content space. The TOC's right strip is filled by `toc_decor.png`, **never** by `logo.jpg`.
- **TOC overrides the section-title slot.** The `Contents` header sits at the TOC's bespoke top anchor; the standard section-title anchor is empty on the TOC.
- **TOC list is one textbox, one column.** Do not create per-item textboxes, do not split numeral and title into separate runs, do not place per-item subtitle lines beneath each section, and do not arrange items into a two-column grid. One textbox, one paragraph per item, one run per paragraph.

## Body Density Strategy

> The body region (Y = 1.62" to Y = 7.20", about 5.58" tall when a subtitle is present — roughly 74% of canvas height) must remain visually populated. Empty bottom-of-slide white space is a design defect, not breathing room.

### Density Targets
- **Visual fill of body region:** 60–80%. Below 60% the slide reads as half-finished; above 80% it loses readability.
- **Vertical balance:** body content extends to within **0.30"–0.50"** of the body region bottom edge (Y ≈ 6.70"–6.90"). Never end body content above Y = 6.00" without an intentional density tactic below it.

### Density Tactics — text-first, cards as last resort

> **Default tactic for every slide is text-first structural composition.** Reach for cards, tiles, or chip layouts only when the content genuinely cannot be expressed as structured prose. The reference deck `Y-PJ-FoRM-2026.pptx` is built almost entirely from layered textboxes, not card grids — match that style.

**Preferred tactics (apply in order):**

1. **Structured prose with sub-headings.** Lead paragraph in `{type.body}` ExtraLight 20pt, followed by labeled sub-sections — each sub-section is a SemiBold-navy heading (`{type.section-subtitle}` or 20pt SemiBold) above an ExtraLight body paragraph. Use vertical rhythm and a small left indent (~0.10"–0.20") to mark hierarchy; no card backgrounds, no border boxes. **This is the default for ~80% of body slides.**
2. **Numbered or labeled lists.** Lines like `1. 선물 포지션 진입 — …` / `2. 듀레이션 매칭 헷지 — …`, set in ExtraLight 20pt with a small navy SemiBold leading numeral or label. Indent the wrap (~0.30") so the numeral hangs. No surrounding box.
3. **Two-column text split.** When two parallel ideas deserve side-by-side treatment, run two text columns at the same Y with a clear vertical gutter (~0.30"). Each column is just a heading + body — **no card border, no fill color, no chip**. The gutter alone separates them.
4. **Anchor figure.** A single chart, equation, or captioned image anchored to the lower-right or full-width band, occupying ~30–50% of body height. Body text reflows around it. The figure carries the system image-shadow if it is a screenshot or render; vector charts have no shadow.
5. **Editorial pull quote.** A SemiBold-navy quotation placed in the lower third, set to ~70% of body width and left-aligned, with a small attribution line in `{type.caption}` beneath. No quote marks, no card.

**Exception tactics (use sparingly, at most one per deck):**

6. **Reference card grid.** Only when the slide is genuinely a list of discrete entities (e.g., a comparison of products, papers, or instruments) where each entity has multiple parallel attributes. Card style: 1px `{colors.hairline}` border, no fill, no shadow. Avoid on narrative slides.
7. **KPI tile strip.** Only when the slide's purpose is to display 3–5 headline metrics (e.g., a results dashboard). Numerals in `{colors.ink-strong}` navy only — never red. Avoid as filler for narrative slides.

### Density Anti-Patterns (do NOT do)
- Do not enlarge the section title or pad the subtitle to fill bottom space — anchors are fixed.
- Do not wrap every paragraph or sub-section in a bordered card. **Bordered containers are the exception, not the default.**
- Do not stack 2–4 card boxes side-by-side as the primary scaffolding for a narrative slide. Use structured prose instead.
- Do not add decorative shapes, dividers, gradients, or icons purely as visual filler.
- Do not stretch line-height or paragraph spacing beyond the typography spec.
- Do not centre-stack short body copy in the middle of the body region — it leaves both top and bottom imbalanced.
- Do not add a logo, watermark, page number, or project mark to "balance" the slide. There are none on standard slides — that's the system.
- Do not bold mid-sentence keywords inside body paragraphs to "emphasize." Bold is reserved for headings, sub-headings, and labeled list items.

### Decision Order (when planning each non-cover slide)
1. Place the section title at the master title anchor.
2. Draw the hairline rule at Y = 0.93".
3. Place the section subtitle (if applicable) at the subtitle anchor.
4. **Draft the body as plain structured prose first** — lead paragraph + 1–3 sub-sections with SemiBold-navy headings + ExtraLight bodies.
5. Measure the residual empty area below the prose.
6. If residual area > 24% of body region, **first** try a numbered list, a sub-section, or an anchor figure. **Only if those don't fit** the content do you reach for a card grid or KPI strip — and only one such block per slide.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| Flat | No shadow, no border | Slide canvas, body text, headlines, the hairline rule |
| Soft hairline | 1px `rgba(0, 0, 0, 0.08)` border | Inline reference cards, data table rows |
| Image shadow | `rgba(0, 0, 0, 0.18) 2px 4px 24px 0` | Charts, figures, or photographic evidence resting on the canvas (the only true "shadow" in the system) |

**Shadow philosophy.** Use **at most one** drop-shadow per slide, applied to a single chart or photograph. Never on cards, never on buttons, never on text, never on the section title. The deck's depth comes from typographic discipline, not elevation.

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | 0pt | Cover hero crop, full-bleed imagery |
| `{rounded.sm}` | 4pt | Inline image radius, compact utility chips |
| `{rounded.md}` | 8pt | Reference cards, KPI tile backgrounds (when filled) |
| `{rounded.lg}` | 12pt | Larger callout cards on body slides |
| `{rounded.pill}` | 999pt | Callout chips inside body copy (used sparingly — no TOC accent chips, the TOC has no chip components) |

### Imagery Geometry
- **Cover hero image:** Two-piece composition — main photograph (10.09" × 6.70") at top-left, complementary strip (3.24" × 0.80") at bottom-right. Both are full-bleed rectangular, no rounding. Reproduced exactly from the reference deck.
- **Body charts and figures:** square or 16:9 crops at `{rounded.md}` (8pt) radius, neutral background, content centred with 0.20"–0.40" internal padding. Apply the system image-shadow if the figure is a screenshot or photograph; vector charts get no shadow.

## Components

### Slide Types

**`slide-cover`** — Cover slide. Bespoke layout per *Cover Anchors*. Built from the same imagery as `Y-PJ-FoRM-2026.pptx` slide 1 (`cover_hero_main.png` + `cover_hero_strip.png` + `logo.jpg`) with the two adjustments codified in *Cover Anchors*: (a) the project title sits **inside the hero photograph** and is **left-aligned**, not centered across the canvas; (b) the logo sits at Y = 1.14" in the white right-hand strip — fully visible, not bleeding above the top edge. The project title (the only editable string) is set in `{type.cover-display}` ExtraBold 40pt. Visual cross-check: attached file `cover_reference.png`.

**`slide-toc`** — Table of contents. **Verbatim reproduction of `Y-PJ-FoRM-2026.pptx` slide 2** per *TOC Anchors*. Layered components (back to front):

1. `toc_decor.png` decorative picture at (10.12", -0.04", 11.29" × 7.50") — fills the right-side strip and intentionally overflows the canvas right edge. **Mandatory.**
2. `Contents` header in **Pretendard SemiBold 50pt** at (0.31", 0.11", 4.51" × 0.94"). Navy or theme text color.
3. Short hairline rule at Y = 1.20" spanning X = 0 to X = 10.12" (0.75pt navy).
4. A single text box at (0.31", 1.34", 9.45" × 3.13") containing the numbered list — one paragraph per section, formatted as `N. Section Name` in **Pretendard ExtraLight 20pt** (navy or theme text). One run per paragraph; numeral and section name are not split.
5. Full-width bottom hairline rule at Y = 6.70" spanning X = 0 to X = 13.33" (0.75pt navy). **Mandatory.**

**TOC items are written in English** even if body slides are Korean. List order need not mirror any textbook order. **No red numerals, no per-item subtitles, no two-column layouts, no Y-FoRM logo, no page number, no project-shortname footer slug — none of these belong on the TOC.**

**`slide-content`** — Standard content slide. Master Anchors apply: section title → hairline rule at Y = 0.93" → subtitle → body. **This is the deck's primary surface — most slides are this type.** Page title (the section-title slot) is **written in English**; the subtitle and body content may be in Korean or English as appropriate. **No top-right logo, no bottom-right page number.**

**`slide-data`** — Data-dense slide. Same chrome as `slide-content` (title + hairline + subtitle + body). The body region is dominated by a single chart or table spanning ~7/12 of the body width with a supporting analysis column on the right (~5/12). Chart carries the system image-shadow if it is a screenshot; vector charts have no shadow. Tables use `{colors.hairline}` row borders and `{type.caption-strong}` headers.

**`slide-quote`** — Editorial pull-quote slide on the standard canvas. Master Anchors apply (title + hairline + subtitle + body). Body region holds a single `{type.body-strong}` quotation centred (or `{type.cover-display}` if the quote should read as a chapter motto), with a small attribution line below in `{type.caption}`.

> **No closing slide.** The deck ends on the final content slide of the final section. Do **not** add a `Thank you`, `Q&A`, contact-info, or "End" slide. Do **not** repeat the cover at the end.
>
> **Forbidden slide types from the predecessor system:** `slide-section-opener` (dark divider), `slide-section-divider`, `slide-content-dark`, `slide-content-parchment`, `slide-fullbleed`, `slide-closing`. The deck is light-only; the cover is the sole full-bleed surface, and section transitions are signaled by the section-title slot alone — no dedicated divider slide.

### Inline Elements

> Inline element components below are **exception components**, not default scaffolding. Default body composition is structured prose with SemiBold-navy sub-headings — see *Density Tactics — text-first, cards as last resort*. Reach for chips/cards/tiles only when the content genuinely requires the form.

**`callout-chip`** — Pill-shaped highlight used in body copy. Background `{colors.primary}` navy at 100% with white text in `{type.caption-strong}`, rounded `{rounded.pill}`, padding 6pt × 12pt. For a softer variant, use `{colors.primary}` at 12% (`rgba(18, 43, 70, 0.12)`) with navy text. **Use sparingly — at most one per slide.**

**`accent-chip`** — **Removed from the active component set.** The reference deck `Y-PJ-FoRM-2026.pptx` uses no red anywhere, including on the TOC. The token is retained as a name only to flag the prior pattern; do not instantiate it on any slide.

**`reference-card`** — Inline rectangular card. Background `{colors.canvas}` white, 1px solid `{colors.hairline}` border, rounded `{rounded.md}` (8pt), padding `{spacing.md}` (0.30"). Holds: an optional small image (1:1 crop with `{rounded.sm}` radius), a heading in `{type.body-strong}`, one line of meta in `{type.body}`, and an optional callout in `{colors.primary}`. **Use only when the slide is genuinely a list of discrete entities with parallel attributes — never as a wrapper for narrative prose.**

**`kpi-tile`** — Compact metric tile. Transparent background, no border, padding 0. Stack: large numeral in `{type.kpi-numeral}` `{colors.ink-strong}` navy → label in `{type.kpi-label}` `{colors.ink-muted}` gray. **Numerals are navy only — never red.** Use only for genuine metrics dashboards, not as visual filler on narrative slides.

**`pull-quote`** — Standalone quotation block. `{type.body-strong}` text in `{colors.ink-strong}` navy, no quote marks, ~70% body width, left-aligned. Attribution beneath in `{type.caption}` `{colors.ink-muted}`.

**`data-table-row`** — Single row of a data table. Bottom border 1px `{colors.hairline}`, vertical padding 0.10". Cell text in `{type.body}`; header row in `{type.caption-strong}` with a heavier bottom border (1px `{colors.ink-muted}`).

**`text-link`** — Inline link in `{colors.primary}` navy, underlined.

### No Footer, No Header

There is no page footer, no header band, no recurring navigation furniture on standard slides. **Do not add page numbers in any format** (no `N`, no `N / NN`, no `Page N`). **Do not add a project short-name slug** in the bottom-left. The body region runs edge-to-edge inside the safe area; the only persistent chrome is the section title and the hairline rule beneath it.

## Asset & Font Embedding (PPTX-specific)

### File Layout (project root)
All filenames below refer to the **exact attached files** listed in the *Required Project Attachments* table at the top of this document.

- `cover_reference.png` — **Reference render of the cover slide** (1920×1080). View this for visual confirmation; never embed it as a flat background.
- `cover_hero_main.png` — Main cover photograph (skyscraper). Insert at cover anchor (0.00", 0.00"), size 10.09" × 6.70".
- `cover_hero_strip.png` — Bottom-right cover strip (complementary crop). Insert at (10.09", 6.70"), size 3.24" × 0.80".
- `logo.jpg` — Y-FoRM identity mark. **Used only on the cover** at (10.58", 1.14"), size 2.27" × 1.70" (per *Cover Anchors*). Do not place on any other slide — including the TOC.
- `PRETENDARD-EXTRALIGHT_0.OTF`, `PRETENDARD-SEMIBOLD.OTF`, `PRETENDARD-EXTRABOLD.OTF` (and the six other weight files) — Pretendard `.OTF` files. Reference Pretendard by name in the `.pptx`; embedding into the file is performed via PowerPoint's native save option, not by the generation pipeline.
- `toc_decor.png` — **Mandatory** decorative right-side graphic on the TOC slide. Insert at (10.12", -0.04"), size 11.29" × 7.50" (intentionally oversized — overflows the right edge; only the leftmost ~3.21" is visible). Do not crop or resize.
- `Y-PJ-FoRM-2026.pptx` — Original reference template. Read for layout reference only; do not link to it from generated decks.

### python-pptx Skeleton
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY  = RGBColor(0x12, 0x2B, 0x46)
RED   = RGBColor(0xC0, 0x00, 0x00)
INK_M = RGBColor(0x7A, 0x7A, 0x7A)

# === COVER ANCHORS ===
# Title sits inside the hero photo (left-aligned). Logo lowered into the
# white right-hand strip — fully visible, not bleeding above the top edge.
COVER_HERO_MAIN   = (Inches(0.00),  Inches(0.00),  Inches(10.09), Inches(6.70))
COVER_HERO_STRIP  = (Inches(10.09), Inches(6.70),  Inches(3.24),  Inches(0.80))
COVER_LOGO        = (Inches(10.58), Inches(1.14),  Inches(2.27),  Inches(1.70))  # cover-only
COVER_TITLE       = (Inches(0.50),  Inches(2.91),  Inches(9.20),  Inches(2.42))  # left-aligned, inside hero
COVER_MEMBERS     = (Inches(0.20),  Inches(6.88),  Inches(9.41),  Inches(0.44))

# === TOC ANCHORS (verbatim from Y-PJ-FoRM-2026.pptx slide 2) ===
# NEVER place logo.jpg on the TOC slide. The right strip is filled by toc_decor.png.
TOC_DECOR         = (Inches(10.12), Inches(-0.04), Inches(11.29), Inches(7.50))  # toc_decor.png; oversized intentionally — overflows right edge
TOC_CONTENTS      = (Inches(0.31),  Inches(0.11),  Inches(4.51),  Inches(0.94))  # 'Contents' — Pretendard SemiBold 50pt
TOC_TOP_RULE      = (Inches(0.00),  Inches(1.20),  Inches(10.12))                 # short rule: X1=0, X2=10.12, Y=1.20
TOC_LIST          = (Inches(0.31),  Inches(1.34),  Inches(9.45),  Inches(3.13))  # ONE textbox, one paragraph per item, ExtraLight 20pt
TOC_BOTTOM_RULE   = (Inches(0.00),  Inches(6.70),  Inches(13.33))                 # full-width: X1=0, X2=13.33, Y=6.70

# === STANDARD CONTENT SLIDE ANCHORS ===
TITLE_X,    TITLE_Y,    TITLE_W,    TITLE_H    = Inches(0.12), Inches(0.09), Inches(13.09), Inches(0.77)
RULE_X1,    RULE_Y,     RULE_X2                = Inches(0.00), Inches(0.93), Inches(13.33)   # hairline
SUB_X,      SUB_Y,      SUB_W,      SUB_H      = Inches(0.14), Inches(1.00), Inches(13.05), Inches(0.55)
BODY_X,     BODY_Y,     BODY_W,     BODY_H     = Inches(0.12), Inches(1.62), Inches(13.09), Inches(5.58)

def draw_hairline(slide, x1=RULE_X1, y=RULE_Y, x2=RULE_X2):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y, x2, y)
    line.line.color.rgb = NAVY
    line.line.width = Pt(0.75)
    return line

def build_toc(slide, sections, decor_path='toc_decor.png'):
    """Build the TOC slide. `sections` is a list of English section names.
    Items are rendered as '1. Name', '2. Name', ... in ONE textbox, ExtraLight 20pt navy."""
    # 1) Right-side decorative picture (intentionally oversized; do NOT place logo.jpg here)
    slide.shapes.add_picture(decor_path, *TOC_DECOR)
    # 2) 'Contents' header — Pretendard SemiBold 50pt (NOT ExtraBold)
    hdr = slide.shapes.add_textbox(*TOC_CONTENTS).text_frame
    r = hdr.paragraphs[0].add_run(); r.text = 'Contents'
    r.font.name = 'Pretendard SemiBold'; r.font.size = Pt(50); r.font.bold = True
    r.font.color.rgb = NAVY
    # 3) Short top rule (X = 0 to 10.12, Y = 1.20)
    draw_hairline(slide, *TOC_TOP_RULE)
    # 4) Numbered list — ONE textbox, one paragraph per item, ExtraLight 20pt
    body = slide.shapes.add_textbox(*TOC_LIST).text_frame
    body.word_wrap = True
    for i, name in enumerate(sections, start=1):
        p = body.paragraphs[0] if i == 1 else body.add_paragraph()
        run = p.add_run(); run.text = f'{i}. {name}'
        run.font.name = 'Pretendard ExtraLight'; run.font.size = Pt(20)
        run.font.color.rgb = NAVY  # NEVER red
    # 5) Full-width bottom rule (X = 0 to 13.33, Y = 6.70)
    draw_hairline(slide, *TOC_BOTTOM_RULE)
```

### Font Embedding
**Do not embed Pretendard programmatically.** Font embedding is delegated to PowerPoint's native option (`File → Options → Save → Embed fonts in the file`). The author's environment is assumed to have Pretendard installed locally; the user enables PowerPoint's embed-fonts setting before saving the final `.pptx`. The generation pipeline references `Pretendard ExtraLight / SemiBold / ExtraBold` by name — actual font binaries are not injected into the output `.pptx` by this prompt.

## Do's and Don'ts

### Do
- Build the cover from the same imagery as `Y-PJ-FoRM-2026.pptx` slide 1 with the two adjustments codified in *Cover Anchors* (title inside the hero photo & left-aligned; logo at Y = 1.14"). Only the project-title text changes between decks.
- Draw the **hairline rule at Y = 0.93", X = 0 to X = 13.33"** on every non-cover slide.
- Follow the four-row anchor stack on every non-cover slide: section title → hairline → subtitle → body.
- **Compose body slides as structured prose first** — lead paragraph + 1–3 SemiBold-navy sub-headings + ExtraLight body. Cards, tiles, and chips are exception components, not the default.
- Use Pretendard for every text element. No exceptions, no secondary typeface.
- Use the active weight ladder **200 / 600 / 800** for all standard slides.
- Use only black + navy + white **on every slide, including the TOC.** The reference deck contains no red.
- Build the TOC by layering `toc_decor.png` (right strip, 10.12", -0.04", 11.29" × 7.50"), the `Contents` SemiBold-50pt header, the short top rule, a single ExtraLight-20pt list textbox, and the full-width bottom rule — exactly as in `Y-PJ-FoRM-2026.pptx` slide 2.
- Set body copy at `{type.body}` (20pt / weight 200 / ExtraLight); shrink to 18pt or 16pt only when content density forces it.
- Apply *Body Density Tactics* whenever residual body region area exceeds 24%, preferring text-first tactics (sub-headings, numbered lists, anchor figures) before card-based tactics.
- Write TOC items and section titles in **English**. Subtitles and body content may be Korean or English as appropriate.
- Reference Pretendard by name (`Pretendard ExtraLight / SemiBold / ExtraBold`); the author enables PowerPoint's native font-embedding option before saving.
- Enable Korean line-break behavior (`word-break: keep-all` equivalent) on every text shape.

### Don't
- **Do not place the Y-FoRM logo (or any "Academic Society" mark) on any non-cover slide — including the TOC.** The logo lives only on the cover. The TOC's right strip is filled by `toc_decor.png`, never by `logo.jpg`.
- **Do not use red anywhere in the deck.** No red text, no red chips, no red numerals, no red rules — on the cover, the TOC, content, data, or quote slides. The reference deck `Y-PJ-FoRM-2026.pptx` contains zero red; match it.
- **Do not split the TOC numeral and section name into separate runs or text boxes.** TOC items are single runs in the form `N. Section Name`, all in the same color and weight (ExtraLight 20pt navy).
- **Do not lay out the TOC as a two-column grid** with per-item numeral boxes, bold titles, and gray subtitles. The TOC is one textbox, single column, ExtraLight 20pt — nothing else.
- **Do not use ExtraBold 800 for the `Contents` header.** It is **SemiBold 600**.
- **Do not bold mid-sentence keywords inside body paragraphs.** Bold is reserved for section titles, subtitles, and clearly labeled sub-section headings (e.g., `예시 —`, `메커니즘`, numbered list labels). Inline emphasis on individual words inside a running paragraph is forbidden.
- **Do not wrap body content in card boxes by default.** Bordered containers (reference cards, KPI tiles, callout chips) are exception components used at most once per slide. Default body composition is structured prose with sub-headings — match the reference deck `Y-PJ-FoRM-2026.pptx` style.
- **Do not stack multiple side-by-side card boxes** ("category boxes" / "feature tiles") as the primary scaffolding for a narrative slide. Use a two-column text split (heading + ExtraLight body, no border) instead.
- **Do not add a page number** (no `N`, no `N / NN`, no `Page N`, no bottom-right counter, no anywhere-else counter) on any slide, **including the TOC**.
- **Do not add a project short-name footer slug** (`Y-PJ-FoRM 39th` or similar) in the bottom-left or anywhere on any slide, **including the TOC**.
- **Do not add a `Thank you`, `Q&A`, `Contact`, or closing slide.** The deck ends on the final content slide.
- **Do not omit the hairline rule** on any non-cover slide. It is the deck's structural signature.
- **Do not center-align the cover title or extend it past the hero photo boundary.** The title is left-aligned and fits inside the hero photograph (right edge ≤ 9.70").
- **Do not use any dark surface** (`#272729`, `#2A2A2C`, etc.). The deck is light-only.
- **Do not introduce a second typeface** for any reason — Pretendard only.
- **Do not introduce a third accent color.** Navy is the only accent in active use; red is forbidden everywhere.
- **Do not use mid-weights** (300 / 400 / 500) in standard slides. The active ladder is 200 / 600 / 800.
- **Do not set the section title or page title in Korean.** TOC and page titles are English; subtitle and body content can be Korean.
- **Do not add shadows to cards, buttons, text, or the hairline.** Shadow is reserved for at most one chart or photograph per slide.
- **Do not use gradients as decorative backgrounds.**
- **Do not centre-stack short body copy** — fill the body region using a density tactic instead.
- **Do not enlarge typography to fill empty bottom space.**
- **Do not shift the master anchors** to balance a slide. If a slide feels empty, fill the body region using *Body Density Strategy* — never move the title, hairline, or subtitle.

## Slide Authoring Checklist

For every slide, verify in order:

1. **Cover discipline:** If this is slide 1, it is built by layering the attached files `cover_hero_main.png`, `cover_hero_strip.png`, and `logo.jpg` at the coordinates in *Cover Anchors*. The project title is **left-aligned and entirely inside the hero photograph** (right edge ≤ 9.70"). The logo sits at Y = 1.14" — not bleeding above the top edge. The result must visually match the attached file `cover_reference.png`.
2. **TOC discipline:** If this is slide 2 (the TOC), it is built by layering exactly five elements per *TOC Anchors*: (a) `toc_decor.png` at (10.12", -0.04", 11.29" × 7.50") — **NOT `logo.jpg`**; (b) `Contents` in **Pretendard SemiBold 50pt** at (0.31", 0.11"); (c) short top rule at Y = 1.20" (X = 0 → 10.12"); (d) **one** textbox at (0.31", 1.34", 9.45" × 3.13") with one ExtraLight 20pt paragraph per section in the form `N. Section Name`; (e) full-width bottom rule at Y = 6.70" (X = 0 → 13.33"). No red, no per-item subtitles, no two-column layout, no logo, no footer, no page number.
3. **No logo on non-cover slides:** No top-right Y-FoRM mark on TOC, content, data, or quote slides. (`logo.jpg` is cover-only.)
4. **Hairline rule:** A 0.75pt navy horizontal line spans X = 0 to X = 13.33" at Y = 0.93" on every non-cover slide. (TOC variant: short rule 10.12" wide at Y = 1.20" + full-width rule at Y = 6.70".)
5. **Anchor stack:** Section title at (0.12", 0.09"), hairline at Y = 0.93", subtitle at (0.14", 1.00"), body region from Y = 1.62" downward. Identical on every non-cover, non-TOC slide.
6. **Single typeface:** All text is Pretendard. No fallback face appears in the rendered output.
7. **Weight ladder:** Every text element uses 200 (ExtraLight), 600 (SemiBold), or 800 (ExtraBold). No 300 / 400 / 500 unless an explicit exception is documented for that slide. Note: the TOC `Contents` header uses **600 (SemiBold)**, not 800.
8. **Palette:** Only black, navy `#122B46`, and white appear on **all** slide types — including the TOC. **No red anywhere** in the deck. TOC numerals are set in the same navy/black as the rest of each item.
9. **Composition style:** Body content is structured prose with SemiBold-navy sub-headings and ExtraLight body — not a grid of bordered card boxes. At most one card / chip / tile component per slide, used only when the content genuinely requires that form.
10. **No inline bold in body paragraphs:** Bold appears only on section titles, subtitles, and clearly labeled sub-section heads (numbered list labels, `예시 —`, `메커니즘`, etc.) — never on individual mid-sentence words.
11. **Body density:** Body region is 60–80% visually populated. If sparse, one density tactic from *Body Density Strategy* has been applied (text-first tactics preferred). Body content extends to within 0.30"–0.50" of the body region bottom edge.
12. **No page numbers, no footer slug:** Confirmed absent in all four corners and along all four edges of every slide, including the TOC.
13. **No closing slide:** The deck does not end with `Thank you`, `Q&A`, `Contact`, or any analogous slide.
14. **Korean line breaks:** Text shapes wrap on 어절 boundaries; no mid-word break and no orphan particles ("이/가/은/는") at line head.

## Input / Output Contract

> The prompt-runner supplies the deck's **content**; this design system supplies the **form**. The contract below defines what input the deck author (Claude) expects and what output it produces.

### Input
- **Project metadata:** `project_name` (English — replaces the cover placeholder), `cohort_year` (e.g., `39th`), `member_roster` (list of `{name, cohort}`).
- **Source content:** The body content the deck must convey — outline, manuscript, or notes (Korean or English).
- **Section plan:** Either an explicit list of section names (English) or instructions to derive one. The TOC need not mirror any source-text order.

### Output
- A single `.pptx` file authored at 13.33" × 7.5", referencing Pretendard by name (200 / 600 / 800 weights minimum), conforming to all anchors and rules in this document. Font embedding is performed by the author through PowerPoint's native save option, not by the generation pipeline.
- Slide order: `slide-cover` → `slide-toc` → (per section: `slide-content` / `slide-data` / `slide-quote` as needed). **The deck terminates on the final content slide — there is no closing slide.**
- Slide count is determined by content density: each section claims enough `slide-content` / `slide-data` slides to convey its argument without violating the body-density bounds.

### Generation Rules
- **Cover generation:** Rebuild the cover by layering the attached files `cover_hero_main.png`, `cover_hero_strip.png`, and `logo.jpg` at the coordinates in *Cover Anchors*, then placing the project-title text and member-roster text on top. Confirm the result visually matches the attached file `cover_reference.png` before emitting. Never insert `cover_reference.png` itself as a slide image.
- **TOC generation:** From the section plan, render numbered items in English. If the source content suggests a section order different from the textbook, prefer the order most useful to the audience.
- **Per-section slide budget:** Aim for 3–6 standard content slides per major section. If a section produces fewer than 3 slides at 60% body density, merge it into a neighbor; if it produces more than 8, split it.
- **English vs Korean:** Section title (top of every body slide) and TOC items must be English. Subtitle and body copy follow the source language; default Korean unless source is English.
- **Density enforcement:** After populating the body region, measure residual empty area. If > 24%, apply exactly one density tactic from *Body Density Strategy* before emitting the slide.
- **Termination:** Stop after the last content slide of the last section. Do not append a closing slide.

## Known Gaps

- Equation rendering (LaTeX → image) is not formalized as a token; insert as a captioned `slide-data` figure with the system image-shadow.
- Citation formatting (footnote vs. inline numbered superscript) is left to the author; both are acceptable in `{type.caption}`.
- Chart styling beyond row-borders and tabular numerals is not formalized; defer to the source library's defaults but force Pretendard as the chart typeface.
- Animation and transitions are out of scope. Static decks only — no slide transitions, no element animations.
- Backup/appendix slides follow the standard content-slide rules; there is no separate `slide-appendix` type.
