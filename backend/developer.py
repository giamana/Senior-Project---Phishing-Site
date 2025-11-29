from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db, get_current_user
from .models import User, Delivery, Simulation
from .schemas import SimulationCreate, AssignRecipients
from .utils import slugify

router = APIRouter(prefix="/dev", tags=["developer"])

def require_developer(user):
    if user.role != "developer":
        raise HTTPException(status_code=403, detail="Forbidden")

@router.get("/recipients")
def recipients(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    user = get_current_user(token, db)
    require_developer(user)
    employees = db.query(User).filter_by(role="employee").all()
    return [{"id": e.id, "name": e.name, "email": e.email, "company_id": e.company_id} for e in employees]

@router.get("/stats")
def stats(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    user = get_current_user(token, db)
    require_developer(user)
    deliveries = db.query(Delivery).all()
    return {
        "total_deliveries": len(deliveries),
        "opened_count": sum(1 for d in deliveries if d.email_opened_at),
        "clicked_count": sum(1 for d in deliveries if d.link_clicked_at)
    }

@router.post("/simulations")
def create_campaign(data: SimulationCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    user = get_current_user(token, db)
    require_developer(user)
    sim = Simulation(
        company_id=None,
        subject=data.subject,
        content=data.content,
        link_slug=slugify(),
        created_by_user_id=user.id
    )
    db.add(sim); db.commit(); db.refresh(sim)
    return {"id": sim.id, "link_slug": sim.link_slug}

@router.post("/simulations/{sim_id}/send")
def send(sim_id: int, data: AssignRecipients, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    user = get_current_user(token, db)
    require_developer(user)
    for rid in data.recipient_ids:
        d = Delivery(simulation_id=sim_id, recipient_user_id=rid)
        db.add(d)
    db.commit()
    return {"dispatched": len(data.recipient_ids)}
