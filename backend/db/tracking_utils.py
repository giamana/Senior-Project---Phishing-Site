import os
import re
import uuid
from typing import Optional


_PLACEHOLDER_PATTERN = re.compile(r"\[([^\]]+)\]")
_CTA_PATTERN = re.compile(r"\[call\s*to\s*action\]", re.IGNORECASE)


def _base_url():
    """
    Tracking links default to http://localhost:5000 but can be overridden with
    the TRACKING_BASE_URL environment variable.
    """
    return os.getenv("TRACKING_BASE_URL", "http://localhost:5000").rstrip("/")


def generate_tracking_token() -> str:
    """Return a unique token that can be embedded in tracking links."""
    return uuid.uuid4().hex


def build_tracking_url(token: str, action: Optional[str] = None) -> str:
    """
    Build a link that points to the tracking service.
    Optional action query parameter differentiates clicks from reports.
    """
    base = _base_url()
    url = f"{base}/track/{token}"
    if action:
        url = f"{url}?action={action}"
    return url


def render_body_with_tracking_links(body: str, click_url: str, report_url: str) -> str:
    """
    Replace the first [Call To Action] placeholder in the template body with the
    click tracking URL and append a reporting link at the bottom.
    """

    def _replacement(match: re.Match[str]) -> str:
        label = match.group(1)
        return f"{label} ({click_url})"

    # Prefer an explicit [Call To Action] placeholder; otherwise fall back to any [label].
    updated_body, count = _CTA_PATTERN.subn(
        f"[Call To Action] ({click_url})", body, count=1
    )
    if count == 0:
        updated_body, count = _PLACEHOLDER_PATTERN.subn(_replacement, body, count=1)

    if count == 0:
        updated_body = f"{body.strip()}\n\nAccess the requested resource: {click_url}"

    updated_body = updated_body.rstrip() + f"\n\nReport this email: {report_url}"
    return updated_body
