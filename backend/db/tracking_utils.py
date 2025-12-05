import html
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
    Replace the first [Call To Action] (or any [label]) with an HTML anchor so
    the CTA text stays visible while the URL is hidden behind the link. Appends
    a reporting link at the bottom. Returns HTML.
    """

    def _anchor(label: str, url: str) -> str:
        safe_label = html.escape(label)
        safe_url = html.escape(url, quote=True)
        return f'<a href="{safe_url}">{safe_label}</a>'

    # Mark the CTA position, then escape the rest of the body so only the anchor renders as HTML.
    marker = "__CTA__"
    chosen_label = "Call To Action"

    marked_body, count = _CTA_PATTERN.subn(marker, body, count=1)
    if count == 0:
        def _mark_placeholder(match: re.Match[str]) -> str:
            nonlocal chosen_label
            chosen_label = match.group(1)
            return marker
        marked_body, count = _PLACEHOLDER_PATTERN.subn(_mark_placeholder, body, count=1)

    if count == 0:
        marked_body = f"{body.strip()}\n\n{marker}"

    escaped_body = html.escape(marked_body)
    with_cta = escaped_body.replace(marker, _anchor(chosen_label, click_url), 1)

    with_report = with_cta.rstrip() + f"<br><br>{_anchor('Report this email', report_url)}"
    return with_report.replace("\n", "<br>")
