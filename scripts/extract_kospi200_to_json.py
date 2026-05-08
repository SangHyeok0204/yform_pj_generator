"""One-shot extractor: capture build_deck.py main() content into DeckContent JSON.

Monkey-patches the build_* functions and Presentation.save before invoking main(),
so no real PPTX is rendered. Output: prompts/examples/kospi200_delta_hedging.json.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build_deck  # noqa: E402

captured = {"cover": None, "toc": None, "slides": []}


def stub_cover(prs, project_title, project_subtitle, member_line):
    captured["cover"] = {
        "title": project_title,
        "subtitle": project_subtitle,
        "member_line": member_line,
    }


def stub_toc(prs, items):
    captured["toc"] = list(items)


def stub_content(prs, title, subtitle, blocks, body_size=18, head_size=20):
    cleaned = []
    for b in blocks:
        kind = b.get("kind", "p")
        out = {"kind": kind}
        if kind == "h":
            out["text"] = b["text"]
        elif kind == "p":
            out["text"] = b["text"]
        elif kind == "li":
            if b.get("num"):
                out["num"] = b["num"]
            if b.get("label"):
                out["label"] = b["label"]
            out["text"] = b.get("text", "")
        elif kind == "gap":
            out["pt"] = b.get("pt", 6)
        elif kind == "caption":
            out["text"] = b["text"]
        if b.get("size") is not None:
            out["size"] = b["size"]
        cleaned.append(out)
    captured["slides"].append(
        {"title": title, "subtitle": subtitle, "blocks": cleaned}
    )


def stub_save(self, *args, **kwargs):
    return None


build_deck.build_cover = stub_cover
build_deck.build_toc = stub_toc
build_deck.build_content = stub_content
build_deck.Presentation.save = stub_save  # avoid writing empty pptx

build_deck.main()

OUT = ROOT / "prompts" / "examples" / "kospi200_delta_hedging.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(captured, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT}  cover_ok={captured['cover'] is not None}  toc={len(captured['toc'])}  slides={len(captured['slides'])}")
