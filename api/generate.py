"""POST /api/generate — main pipeline endpoint.

Multipart form fields:
  file        : .pdf or .docx upload
  title       : cover title
  subtitle    : cover one-line subtitle
  member_line : cover member roster

Headers:
  Authorization: Bearer <SITE_TOKEN>

Returns: application/vnd.openxmlformats-officedocument.presentationml.presentation
(the rendered .pptx as a stream).
"""
import re
from typing import Annotated, Optional
from urllib.parse import quote

from anthropic import APIError, RateLimitError
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import ValidationError

from ._lib.auth import verify_token
from ._lib.engine import render_deck
from ._lib.extract.docx import extract_docx_text
from ._lib.extract.pdf import extract_pdf_text
from ._lib.llm import generate_deck_content

app = FastAPI(title="Y-PJ-FoRM Deck Generator")

PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
SAFE_NAME = re.compile(r"[^\w\-가-힣]+")


def _safe_filename(title: str) -> str:
    base = SAFE_NAME.sub("_", title).strip("_")[:60] or "deck"
    return f"{base}.pptx"


def _content_disposition(title: str) -> str:
    name = _safe_filename(title)
    ascii_fallback = re.sub(r"[^\x20-\x7e]+", "_", name).strip("_") or "deck.pptx"
    encoded = quote(name, safe="")
    return f"attachment; filename=\"{ascii_fallback}\"; filename*=UTF-8''{encoded}"


@app.post("/api/generate")
async def generate(
    file: Annotated[UploadFile, File(...)],
    title: Annotated[str, Form(...)],
    subtitle: Annotated[str, Form(...)],
    member_line: Annotated[str, Form(...)],
    authorization: Annotated[Optional[str], Header()] = None,
) -> Response:
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="Invalid or missing site token")

    filename = (file.filename or "").lower()
    data = await file.read()
    if filename.endswith(".pdf"):
        try:
            paper_text = extract_pdf_text(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"PDF 추출 실패: {e}") from e
    elif filename.endswith(".docx"):
        try:
            paper_text = extract_docx_text(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"DOCX 추출 실패: {e}") from e
    else:
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 형식입니다. .pdf 또는 .docx만 허용됩니다.",
        )

    if len(paper_text.strip()) < 200:
        raise HTTPException(
            status_code=400,
            detail=f"추출된 본문이 너무 짧습니다 ({len(paper_text)} chars). 다른 파일을 시도해주세요.",
        )

    try:
        content = generate_deck_content(
            paper_text=paper_text,
            metadata={"title": title, "subtitle": subtitle, "member_line": member_line},
        )
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail="Anthropic API 한도 초과. 잠시 후 다시 시도해주세요.") from e
    except ValidationError as e:
        raise HTTPException(status_code=502, detail=f"LLM이 생성한 콘텐츠 스키마 검증 실패: {e.errors()}") from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API 오류: {e.message}") from e

    pptx_bytes = render_deck(content)

    return Response(
        content=pptx_bytes,
        media_type=PPTX_MIME,
        headers={
            "Content-Disposition": _content_disposition(title),
            "X-Slide-Count": str(len(content.slides) + 2),
        },
    )
