from fastapi import APIRouter
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from datetime import datetime
from .database import SessionLocal
from .models import Simulation, Delivery

router = APIRouter(tags=["tracking"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/t/{slug}")
def track_click(slug: str, d: int = None):
    db = next(get_db())
    sim = db.query(Simulation).filter_by(link_slug=slug).first()
    if sim and d:
        delivery = db.query(Delivery).filter_by(id=d).first()
        if delivery:
            delivery.link_clicked_at = datetime.utcnow()
            db.commit()
    return RedirectResponse(url="https://example.com/thanks")  # change landing

@router.get("/o/{delivery_id}")
def track_open(delivery_id: int):
    db = next(get_db())
    delivery = db.query(Delivery).filter_by(id=delivery_id).first()
    if delivery:
        delivery.email_opened_at = datetime.utcnow()
        db.commit()
    # 1x1 gif pixel (transparent)
    gif_1x1 = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    return Response(content=gif_1x1, media_type="image/gif")
