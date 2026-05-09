"""Smoke-test that schema validators and engine overflow guard fire correctly."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api._lib.engine import (
    BODY_H,
    BODY_W,
    SlideOverflowError,
    build_content,
    _fit_body_size,
)
from api._lib.schema import (
    HeadingBlock,
    ListItemBlock,
    ParagraphBlock,
    Slide,
)
from pptx import Presentation
from pptx.util import Inches

OUT = Path(r"C:\temp_decks\guard_tests.txt")
lines: list[str] = []


def case(name, fn):
    try:
        fn()
        lines.append(f"FAIL [{name}] — no exception")
    except (ValueError, SlideOverflowError) as e:
        lines.append(f"PASS [{name}] — {type(e).__name__}: {str(e)[:160]}")


def case_should_pass(name, fn):
    try:
        fn()
        lines.append(f"PASS [{name}] — no exception")
    except (ValueError, SlideOverflowError) as e:
        lines.append(f"FAIL [{name}] — {type(e).__name__}: {str(e)[:160]}")


# Schema validators
case(
    "5 headings > cap 4",
    lambda: Slide(title="T", blocks=[HeadingBlock(text=f"H{i}") for i in range(5)]),
)
case(
    "1200 char body > cap 1100",
    lambda: Slide(title="T", blocks=[ParagraphBlock(text="가" * 1200)]),
)
case(
    "10 list items > cap 9",
    lambda: Slide(title="T", blocks=[ListItemBlock(text=f"i{i}") for i in range(10)]),
)
case(
    "avg paragraph 200 > cap 180",
    lambda: Slide(
        title="T",
        blocks=[ParagraphBlock(text="가" * 200), ParagraphBlock(text="가" * 200)],
    ),
)
case_should_pass(
    "legal slide (1 H + 1 P @ 100 chars)",
    lambda: Slide(
        title="T", blocks=[HeadingBlock(text="ok"), ParagraphBlock(text="가" * 100)]
    ),
)


# Engine overflow guard — build a slide with too many wide paragraphs to overflow at 14pt
# Each P is 175 chars (just under avg cap), 6 of them => 1050 chars total (under 1100 cap),
# but 6 * (~3 lines @ 14pt) ~= 6 * 53pt = 318pt = 4.42" plus spacing — close to limit.
# Add 4 H + extra LIs to push past 14pt fit.
overflow_blocks = [
    HeadingBlock(text="A" * 30),
    ParagraphBlock(text="가" * 175),
    HeadingBlock(text="B" * 30),
    ParagraphBlock(text="가" * 175),
    HeadingBlock(text="C" * 30),
    ParagraphBlock(text="가" * 175),
    HeadingBlock(text="D" * 30),
    ParagraphBlock(text="가" * 175),
    ListItemBlock(text="가" * 80, num="1."),
    ListItemBlock(text="가" * 80, num="2."),
    ListItemBlock(text="가" * 80, num="3."),
]
overflow_slide = Slide(
    title="OverflowTest", subtitle="overflow test", blocks=overflow_blocks
)


def render_overflow():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blocks = [b.model_dump() for b in overflow_slide.blocks]
    build_content(prs, overflow_slide.title, overflow_slide.subtitle, blocks)


# Check whether this overflow_slide actually overflows at 14pt — if not, skip
body_w_in = BODY_W / 914400
max_h_in = BODY_H / 914400
hd, bd, est = _fit_body_size(
    [b.model_dump() for b in overflow_slide.blocks], body_w_in, max_h_in
)
lines.append(
    f"\n[overflow probe] est at body={bd}pt = {est:.2f}\" vs max={max_h_in:.2f}\""
)
if est > max_h_in:
    case("engine SlideOverflowError (intentional overflow)", render_overflow)
else:
    lines.append("(overflow_slide did not actually overflow — skipping engine guard test)")


OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"-> {OUT}  ({len(lines)} lines)")
for l in lines:
    try:
        print(l)
    except UnicodeEncodeError:
        print(l.encode("ascii", "replace").decode("ascii"))
