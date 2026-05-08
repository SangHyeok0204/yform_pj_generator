"""PDF text extraction via pymupdf (fitz)."""
from __future__ import annotations

import fitz


def extract_pdf_text(data: bytes) -> str:
    """Return full text of a PDF as a single string, page-separated."""
    doc = fitz.open(stream=data, filetype="pdf")
    try:
        pages = []
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                pages.append(text.strip())
        return "\n\n".join(pages)
    finally:
        doc.close()
