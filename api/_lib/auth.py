"""Pre-shared token authentication."""
from __future__ import annotations

import hmac
import os


def _extract_bearer(header: str | None) -> str:
    if not header:
        return ""
    parts = header.split(None, 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()
    return header.strip()


def verify_token(authorization_header: str | None) -> bool:
    """Constant-time compare an Authorization header against SITE_TOKEN."""
    expected = os.environ.get("SITE_TOKEN", "")
    provided = _extract_bearer(authorization_header)
    if not expected or not provided:
        return False
    return hmac.compare_digest(provided.encode("utf-8"), expected.encode("utf-8"))
