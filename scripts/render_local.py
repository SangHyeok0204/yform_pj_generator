"""Local regression render: load a JSON example through the new engine and
write a PPTX next to the original under reference/past_outputs/ for diff.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api._lib.engine import render_deck
from api._lib.schema import DeckContent

EXAMPLE = ROOT / "prompts" / "examples" / "kospi200_delta_hedging.json"
OUT = ROOT / "reference" / "past_outputs" / "Y-PJ-FoRM_KOSPI200_DeltaHedging__regen.pptx"


def main():
    raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    content = DeckContent.model_validate(raw)
    pptx_bytes = render_deck(content)
    OUT.write_bytes(pptx_bytes)
    print(
        f"rendered {len(pptx_bytes):,} bytes -> {OUT.relative_to(ROOT)}"
        f"  ({len(content.slides) + 2} slides)"
    )


if __name__ == "__main__":
    main()
