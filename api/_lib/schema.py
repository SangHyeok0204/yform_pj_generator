"""DeckContent schema.

Structured output that the LLM produces and the engine consumes.
Mirrors the block grammar of prompts/design_system.md without prescribing
visuals (those live in engine.py).
"""
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class Cover(BaseModel):
    title: str = Field(description="Project title shown on the cover slide.")
    subtitle: str = Field(description="One-line subtitle under the title.")
    member_line: str = Field(
        description=(
            "Member roster line at the bottom of the cover slide, e.g. "
            "'Hu · Kirilova · Muravyev · Ryu (2025) | Reviewed by Y-FoRM'."
        )
    )


class HeadingBlock(BaseModel):
    kind: Literal["h"] = "h"
    text: str = Field(description="SemiBold-navy sub-section heading.")
    size: Optional[int] = None


class ParagraphBlock(BaseModel):
    kind: Literal["p"] = "p"
    text: str = Field(description="Body paragraph in ExtraLight ink black.")
    size: Optional[int] = None


class ListItemBlock(BaseModel):
    kind: Literal["li"] = "li"
    num: Optional[str] = Field(
        default=None,
        description="Marker token, e.g. '1.', 'STEP 1', '·', 'A.'.",
    )
    label: Optional[str] = Field(
        default=None,
        description="Bold label rendered before an em dash separator.",
    )
    text: str
    size: Optional[int] = None


class GapBlock(BaseModel):
    kind: Literal["gap"] = "gap"
    pt: int = 6


class CaptionBlock(BaseModel):
    kind: Literal["caption"] = "caption"
    text: str
    size: Optional[int] = None


Block = Annotated[
    Union[HeadingBlock, ParagraphBlock, ListItemBlock, GapBlock, CaptionBlock],
    Field(discriminator="kind"),
]


class Slide(BaseModel):
    title: str = Field(
        description="Section title, e.g. '3. Profitability of OMMs'."
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="Sub-section line, e.g. '3.1 수익성 — ...'.",
    )
    blocks: list[Block]


class DeckContent(BaseModel):
    cover: Cover
    toc: list[str] = Field(
        description="Table of contents items, one per major section."
    )
    slides: list[Slide]
