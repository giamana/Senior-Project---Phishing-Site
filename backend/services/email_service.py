# backend/services/email_service.py
import uuid
from datetime import datetime
from typing import Any, Optional
from sqlalchemy.orm import Session

from ..models import EmailTemplate, EmailSent, Employee, User, Role

TRACK_BASE_URL = "http://localhost:8000/api/track/"  # adjust for production

def _get_subject_and_body(payload: Any) -> tuple[str, str]:
    """
    Accept either an EmailTemplate-like object (has .subject/.body)
    or a simple dict-like payload (has 'subject'/'body' keys).
    """
    if hasattr(payload, "subject") and hasattr(payload, "body"):
        return payload.subject, payload.body
    # fallback for dict-like payloads
    subject = payload.get("subject") if isinstance(payload, dict) else ""
    body = payload.get("body") if isinstance(payload, dict) else ""
    return subject or "", body or ""

def send_email_to_employee(
    db: Session,
    sender: User,                    # employer or developer
    employee: Employee,
    template_or_payload: Any         # EmailTemplate or EmailCreate-like dict/object
) -> str:
    """
    Create an EmailSent row with a unique tracking URL and return that URL.
    This function does not perform SMTP sending; integrate SMTP separately if needed.
    """
    unique_id = uuid.uuid4().hex
    subject, body = _get_subject_and_body(template_or_payload)

    # Determine sender role ids (use lowercase enum values)
    employer_id: Optional[int] = None
    developer_id: Optional[int] = None
    try:
        role_value = sender.role.value if hasattr(sender.role, "value") else str(sender.role).lower()
    except Exception:
        role_value = str(sender.role).lower()

    if role_value == "employer":
        employer_id = sender.id
    elif role_value == "developer":
        developer_id = sender.id

    email_sent = EmailSent(
        employee_id=employee.id,
        employer_id=employer_id,
        developer_id=developer_id,
        template_id=getattr(template_or_payload, "id", None),
        unique_url_id=unique_id,
        subject=subject,
        body=body,
        created_at=datetime.utcnow(),
    )

    db.add(email_sent)
    db.commit()
    db.refresh(email_sent)

    return f"{TRACK_BASE_URL}{unique_id}"
