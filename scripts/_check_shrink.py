"""For every content slide, compute the body_size that _fit_body_size picks,
so we can see which slides triggered auto-shrink (16 or 14pt).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api._lib.engine import (
    BODY_H,
    BODY_W,
    SHRINK_LADDER,
    _estimate_blocks_height_in,
    _fit_body_size,
)
from scripts.build_kospi200_mm import ALL_SLIDES

OUT = Path(r"C:\temp_decks\shrink_report.txt")

body_w_in = BODY_W / 914400
max_h_in = BODY_H / 914400

lines = [f"body_w={body_w_in:.2f}\"  max_h={max_h_in:.2f}\""]
shrink_count = {18: 0, 16: 0, 14: 0}
for i, slide in enumerate(ALL_SLIDES, start=3):
    blocks = [b.model_dump() for b in slide.blocks]
    head, body, est = _fit_body_size(blocks, body_w_in, max_h_in)
    # Also compute estimates at all 3 sizes for visibility
    ests = []
    for h, b in SHRINK_LADDER:
        e = _estimate_blocks_height_in(blocks, b, h, body_w_in)
        ests.append(f"{b}pt={e:.2f}\"")
    flag = ""
    if est > max_h_in:
        flag = " ❌OVERFLOW"
    elif body < 18:
        flag = f" ⤓shrunk→{body}pt"
    shrink_count[body] += 1
    lines.append(
        f"slide{i:02d} body={body}pt est={est:.2f}\" "
        f"[{', '.join(ests)}] — {slide.title} | {slide.subtitle or ''}{flag}"
    )

lines.append("")
lines.append(
    f"summary: {shrink_count[18]} at 18pt, "
    f"{shrink_count[16]} at 16pt, {shrink_count[14]} at 14pt"
)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"-> {OUT}")
