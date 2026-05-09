"""DeckContent schema + planning pipeline schema.

Stages (see prompts/slide_planning.md):
    Stage 1 (Outline)     -> SectionOutline
    Stage 2 (Slide Plan)  -> SlidePlan
    Stage 3 (Content)     -> Slide.blocks
    Render                -> DeckContent (cover + toc + slides)

Hard density caps (see prompts/density_caps.md) are enforced on Slide:
    body chars      <= 1100
    h blocks        <= 4
    li blocks       <= 9
    avg p length    <= 180
"""
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator


# === Density caps (kept in lockstep with prompts/density_caps.md) ===
CAP_BODY_CHARS = 1100
CAP_HEADINGS = 4
CAP_LIST_ITEMS = 9
CAP_AVG_PARAGRAPH = 180


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

    @model_validator(mode="after")
    def _check_density_caps(self) -> "Slide":
        """Enforce density caps from prompts/density_caps.md.

        Catches over-stuffed slides at construction time so the LLM/author
        is forced back to slide_planning.md Stage 2 to split the slide.
        """
        body_chars = 0
        n_h = 0
        n_li = 0
        p_lengths: list[int] = []
        for blk in self.blocks:
            text = getattr(blk, "text", "") or ""
            body_chars += len(text)
            if isinstance(blk, HeadingBlock):
                n_h += 1
            elif isinstance(blk, ListItemBlock):
                n_li += 1
                if blk.label:
                    body_chars += len(blk.label)
                if blk.num:
                    body_chars += len(blk.num)
            elif isinstance(blk, ParagraphBlock):
                p_lengths.append(len(text))
        avg_p = sum(p_lengths) / len(p_lengths) if p_lengths else 0

        errs: list[str] = []
        if body_chars > CAP_BODY_CHARS:
            errs.append(f"본문 총 글자 {body_chars} > {CAP_BODY_CHARS}")
        if n_h > CAP_HEADINGS:
            errs.append(f"헤딩 블록 {n_h} > {CAP_HEADINGS}")
        if n_li > CAP_LIST_ITEMS:
            errs.append(f"리스트 아이템 {n_li} > {CAP_LIST_ITEMS}")
        if avg_p > CAP_AVG_PARAGRAPH:
            errs.append(f"단락 평균 길이 {avg_p:.0f} > {CAP_AVG_PARAGRAPH}")

        if errs:
            raise ValueError(
                f"slide '{self.title}' 캡 위반 — " + "; ".join(errs)
                + ". 슬라이드 분할 또는 본문 축약 필요 (prompts/slide_planning.md 참조)."
            )
        return self


class DeckContent(BaseModel):
    cover: Cover
    toc: list[str] = Field(
        description="Table of contents items, one per major section."
    )
    slides: list[Slide]


# === Stage 1+2 — Slide Planning Pipeline ===


class SectionOutline(BaseModel):
    """Stage 1 (Outline) — one major TOC section."""

    n: int = Field(description="Section number (1, 2, 3, ...).")
    title_en: str = Field(
        description="English section title, used as both TOC item and per-slide section-title."
    )
    summary: str = Field(
        description="What this section covers (1-2 Korean sentences). LLM self-check, not rendered."
    )
    target_slides: int = Field(
        ge=1,
        le=10,
        description="Recommended slide count for this section (3-6 typical).",
    )


class SlidePlan(BaseModel):
    """Stage 2 (Slide Plan) — one slide's plan before content is filled in."""

    section_n: int = Field(description="Owning section's `n`.")
    slide_idx_in_section: int = Field(ge=1, description="1-based index within the section.")
    title: str = Field(description="`N. Section Name` — same as SectionOutline.title_en, prefixed.")
    subtitle: str = Field(
        description="`N.M Sub-section Name — short description` form."
    )
    one_idea: str = Field(
        description=(
            "The single message this slide carries (1-2 Korean sentences). "
            "If two messages are needed, split into two SlidePlans."
        )
    )
    source_refs: list[str] = Field(
        default_factory=list,
        description="Source references — docx paragraph indices, pdf pages, URLs, etc.",
    )


class DeckPlan(BaseModel):
    """Stage 1+2 combined output — section outline + per-slide plan.

    Validated to keep the two stages consistent: each SectionOutline.target_slides
    must equal the number of SlidePlans whose section_n matches.
    """

    cover: Cover
    sections: list[SectionOutline]
    slides: list[SlidePlan]

    @model_validator(mode="after")
    def _check_section_slide_consistency(self) -> "DeckPlan":
        section_ns = {s.n for s in self.sections}
        # Stage 2 cannot reference an unknown section
        for sp in self.slides:
            if sp.section_n not in section_ns:
                raise ValueError(
                    f"SlidePlan(section_n={sp.section_n}) references unknown section. "
                    f"Known sections: {sorted(section_ns)}."
                )
        # Stage 1's target_slides must match Stage 2's actual count
        for sec in self.sections:
            actual = sum(1 for sp in self.slides if sp.section_n == sec.n)
            if actual != sec.target_slides:
                raise ValueError(
                    f"section {sec.n} ({sec.title_en!r}): target_slides={sec.target_slides} "
                    f"but {actual} SlidePlans found. Reconcile Stage 1 ↔ Stage 2."
                )
        # slide_idx_in_section must be 1..N contiguous within each section
        for sec in self.sections:
            idxs = sorted(
                sp.slide_idx_in_section for sp in self.slides if sp.section_n == sec.n
            )
            expected = list(range(1, sec.target_slides + 1))
            if idxs != expected:
                raise ValueError(
                    f"section {sec.n}: slide_idx_in_section {idxs} != expected {expected}"
                )
        return self
