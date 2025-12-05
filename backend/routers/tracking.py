
# backend/routers/tracking.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# ✅ import from parent package
from ..database import get_db
from ..models import EmailSent, ClickEvent


router = APIRouter()

@router.get("/track/{unique_url_id}")
def track_click(unique_url_id: str, db: Session = Depends(get_db)):
    email_sent = db.query(EmailSent).filter(EmailSent.unique_url_id == unique_url_id).first()
    if not email_sent:
        raise HTTPException(status_code=404, detail="Tracking token not found")
    click = ClickEvent(email_id=email_sent.id, employee_id=email_sent.employee_id)
    db.add(click)
    db.commit()
    return {"tracked": True, "emailSentId": email_sent.id, "clicks": len(email_sent.clicks)}
