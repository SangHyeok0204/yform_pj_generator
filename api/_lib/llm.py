"""Anthropic Claude Opus 4.7 wrapper.

Converts paper text + presentation metadata into a validated DeckContent
object. Uses prompt caching on the design system + few-shot example so
repeat calls share a cached prefix, and tool_use to force schema-conformant
JSON output.
"""
from __future__ import annotations

import os
from pathlib import Path

from anthropic import Anthropic

from .schema import DeckContent

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"

MODEL = "claude-opus-4-7"

SYSTEM_INTRO = """당신은 Y-PJ-FoRM 학회의 학술 발표자료 디자인 시스템에 따라
학술 논문 또는 발표 개요 문서를 PowerPoint 발표자료의 구조화된 콘텐츠로
변환하는 전담 도우미입니다.

# 작업 원칙
1. 첨부된 디자인 시스템(`design_system.md`)의 슬라이드 문법을 엄격히 따른다.
2. 결과 deck은 cover + toc + 7~9개의 content 슬라이드로 구성한다.
   각 content 슬라이드는 본문 영역의 60~80% 밀도로 채운다 — 빈 하단부는 결함이다.
3. 블록 종류:
   - `h`: 네이비 SemiBold 소제목 (예: "마이크로스트럭처 이론의 시각")
   - `p`: 검정 ExtraLight 본문 단락
   - `li`: 번호/라벨/설명 리스트 항목 (`num`, `label`, `text`)
   - `gap`: 수직 간격 (특수한 경우에만)
   - `caption`: 표·그림 캡션
4. 절대 금지:
   - 본문 단락 내 굵게 강조 금지 — 굵게는 소제목과 li 라벨에만 적용된다.
   - 빨간색 사용 금지 (모든 슬라이드).
   - 한국어/영어 혼용 시 자연스러운 한국어 우선, 고유명사·전문용어만 영문 유지.
5. 슬라이드 제목은 `N. 섹션명`, 부제는 `N.M 소절제목 — 한 줄 설명` 형태를 따른다.
6. 표지(cover)의 title/subtitle/member_line은 사용자가 제공한 메타데이터를
   그대로 사용한다. 임의 변경 금지.
7. 결과는 반드시 `submit_deck_content` 툴을 호출하여 제출한다.
   추가 설명 텍스트는 출력하지 않는다.
"""


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


SUBMIT_TOOL = {
    "name": "submit_deck_content",
    "description": (
        "Submit the structured DeckContent for the deck. Call this exactly "
        "once with the complete deck content (cover + toc + content slides)."
    ),
    "input_schema": DeckContent.model_json_schema(),
}


def generate_deck_content(
    paper_text: str,
    metadata: dict,
    *,
    api_key: str | None = None,
) -> DeckContent:
    """Convert paper text + metadata to a validated DeckContent.

    Parameters
    ----------
    paper_text : str
        Extracted body text from the user's PDF/DOCX upload.
    metadata : dict
        Must contain keys ``title``, ``subtitle``, ``member_line``.

    Raises
    ------
    RuntimeError
        If Claude does not produce a tool call.
    pydantic.ValidationError
        If the tool input does not match DeckContent.
    """
    client = Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])

    design_system = _load_text(PROMPTS_DIR / "design_system.md")
    example_json = _load_text(PROMPTS_DIR / "examples" / "kospi200_delta_hedging.json")

    system_blocks = [
        {"type": "text", "text": SYSTEM_INTRO},
        {
            "type": "text",
            "text": "=== Design System (prompts/design_system.md) ===\n\n" + design_system,
        },
        {
            "type": "text",
            "text": (
                "=== Reference Example DeckContent ===\n"
                "아래 JSON은 KOSPI 200 델타헷지 논문을 변환한 결과이며,\n"
                "슬라이드 분할·밀도·블록 사용 패턴의 정답이다.\n\n"
                + example_json
            ),
            "cache_control": {"type": "ephemeral"},
        },
    ]

    user_message = (
        "다음 자료를 학회 발표자료로 변환해주세요.\n\n"
        "# 표지에 사용할 메타데이터 (그대로 사용)\n"
        f"- title: {metadata['title']}\n"
        f"- subtitle: {metadata['subtitle']}\n"
        f"- member_line: {metadata['member_line']}\n\n"
        "# 원문 자료\n"
        f"{paper_text}\n\n"
        "위 원문을 분석해 cover + toc + content 슬라이드로 구성된 DeckContent를 "
        "`submit_deck_content` 툴로 제출하세요."
    )

    with client.messages.stream(
        model=MODEL,
        max_tokens=32000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=system_blocks,
        tools=[SUBMIT_TOOL],
        tool_choice={"type": "tool", "name": "submit_deck_content"},
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        message = stream.get_final_message()

    for block in message.content:
        if block.type == "tool_use" and block.name == "submit_deck_content":
            return DeckContent.model_validate(block.input)

    raise RuntimeError(
        f"Claude did not call submit_deck_content (stop_reason={message.stop_reason})"
    )
