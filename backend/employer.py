from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db, get_current_user
from .models import User, Delivery, Simulation
from .schemas import SimulationCreate, AssignRecipients
from .utils import slugify

router = APIRouter(prefix="/employer", tags=["employer"])

def require_employer(user: User):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")

def get_token_from_header(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.split(" ")[1]

@router.get("/employees")
def list_employees(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employer(user)
    employees = db.query(User).filter_by(company_id=user.company_id, role="employee").all()
    return [{"id": e.id, "name": e.name, "email": e.email} for e in employees]

@router.post("/employees")
def add_employee(name: str, email: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employer(user)
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    employee = User(name=name, email=email, password_hash="!", role="employee", company_id=user.company_id)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return {"id": employee.id, "name": employee.name, "email": employee.email}

@router.post("/simulations")
def create_simulation(data: SimulationCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employer(user)
    sim = Simulation(
        company_id=user.company_id,
        subject=data.subject,
        content=data.content,
        link_slug=slugify(),
        created_by_user_id=user.id
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)
    return {"id": sim.id, "link_slug": sim.link_slug}

@router.post("/simulations/{sim_id}/assign")
def assign(sim_id: int, data: AssignRecipients, authorization: str = Header(None), db: Session = Depends(get_db)):
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employer(user)
    for rid in data.recipient_ids:
        d = Delivery(simulation_id=sim_id, recipient_user_id=rid)
        db.add(d)
    db.commit()
    return {"assigned": len(data.recipient_ids)}

@router.get("/stats")
def stats(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = get_token_from_header(authorization)
    user = get_current_user(token, db)
    require_employer(user)
    employees = db.query(User).filter_by(company_id=user.company_id, role="employee").all()
    emp_ids = [e.id for e in employees]
    deliveries = db.query(Delivery).filter(Delivery.recipient_user_id.in_(emp_ids)).all()
    return {
        "employees_count": len(employees),
        "total_deliveries": len(deliveries),
        "opened_count": sum(1 for d in deliveries if d.email_opened_at),
        "clicked_count": sum(1 for d in deliveries if d.link_clicked_at)
    }
