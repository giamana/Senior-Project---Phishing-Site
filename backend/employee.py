from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from .deps import get_db, get_current_user
from .models import User, Delivery, Simulation

router = APIRouter(prefix="/employee", tags=["employee"])


def require_employee(user: User) -> None:
    """Ensure the current user has the employee role."""
    if user.role != "employee":
        raise HTTPException(status_code=403, detail="Forbidden")


def get_token_from_header(authorization: str | None) -> str:
    """Extract Bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.split(" ")[1]


@router.get("/stats")
def employee_stats(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> Dict[str, int]:
    """Return phishing stats for the logged-in employee."""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employee(user)

    deliveries: List[Delivery] = db.query(Delivery).filter_by(recipient_user_id=user.id).all()

    return {
        "total_deliveries": len(deliveries),
        "opened_count": sum(1 for d in deliveries if d.email_opened_at),
        "clicked_count": sum(1 for d in deliveries if d.link_clicked_at),
    }


@router.get("/simulations")
def employee_simulations(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """Return simulations associated with the logged-in employee."""
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employee(user)

    deliveries: List[Delivery] = db.query(Delivery).filter_by(recipient_user_id=user.id).all()

    sims: List[Simulation] = []
    for d in deliveries:
        sim = db.get(Simulation, d.simulation_id)  # ✅ modern SQLAlchemy 2.0 style
        if sim:
            sims.append(sim)

    return [
        {
            "id": s.id,
            "subject": s.subject,
            "content": s.content,
            "link_slug": s.link_slug,
        }
        for s in sims
    ]
