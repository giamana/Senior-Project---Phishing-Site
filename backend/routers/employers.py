from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..deps import auth_required, require_role
from ..models import User, Role, Employee, EmailSent, ClickEvent
from ..schemas import EmployerStatsOut, EmployeeCreate, EmailCreate
from ..services.email_service import send_email_to_employee
from ..auth import hash_password

router = APIRouter()

@router.get("/employer/{employer_id}/employees")
def employer_employees(employer_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    if user.role == Role.employer and user.id != employer_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    emps = db.query(Employee).filter(Employee.employer_id == employer_id).all()
    rows = []
    for emp in emps:
        emails_sent = db.query(EmailSent).filter(EmailSent.employee_id == emp.id).count()
        urls_clicked = db.query(ClickEvent).filter(ClickEvent.employee_id == emp.id).count()
        employee_user = db.get(User, emp.user_id)
        rows.append({
            "id": emp.id,
            "userId": emp.user_id,
            "first_name": employee_user.first_name,
            "last_name": employee_user.last_name,
            "emailsSent": emails_sent,
            "urlsClicked": urls_clicked,
        })
    return {"employees": rows}

@router.post("/employer/{employer_id}/add-employee")
def add_employee(employer_id: int, body: EmployeeCreate, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.employer])
    if user.id != employer_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    existing_user = db.query(User).filter(User.email == body.email.lower()).first()
    if existing_user:
        if existing_user.role != Role.employee:
            raise HTTPException(status_code=400, detail="User exists but is not an employee")
        # link existing employee to this employer/company
        emp = db.query(Employee).filter(Employee.user_id == existing_user.id).first()
        if not emp:
            emp = Employee(user_id=existing_user.id, employer_id=employer_id, company_id=user.company.id if user.company else None)
            db.add(emp)
        else:
            emp.employer_id = employer_id
            emp.company_id = user.company.id if user.company else None
        db.commit()
        return {"linked": True, "employeeUserId": existing_user.id, "companyId": emp.company_id}

    # otherwise create new employee user
    employee_user = User(
        first_name=body.first_name,
        last_name=body.last_name or "",
        email=body.email.lower(),
        hashed_password=hash_password("temporary_password_please_reset"),
        role=Role.employee,
    )
    db.add(employee_user)
    db.commit()
    db.refresh(employee_user)

    company_id = user.company.id if user.company else None
    new_emp = Employee(user_id=employee_user.id, employer_id=employer_id, company_id=company_id)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {"linked": True, "employeeUserId": employee_user.id, "companyId": company_id}

@router.post("/employer/{employer_id}/send-email/{employee_id}")
def employer_send_email(employer_id: int, employee_id: int, body: EmailCreate, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.employer])
    if user.id != employer_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    employee = db.get(Employee, employee_id)
    if not employee or employee.employer_id != employer_id:
        raise HTTPException(status_code=404, detail="Employee not found")

    track_url = send_email_to_employee(db, user, employee, body)
    return {"sent": True, "trackUrl": track_url}

@router.delete("/employer/{employer_id}/delete-employee/{employee_id}")
def employer_delete_employee(employer_id: int, employee_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.employer])
    if user.id != employer_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    emp = db.get(Employee, employee_id)
    if not emp or emp.employer_id != employer_id:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return {"deleted": True, "employeeId": employee_id}

@router.get("/employer/{employer_id}/stats", response_model=EmployerStatsOut)
def employer_stats(employer_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.employer])
    if user.id != employer_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    total_employees = db.query(Employee).filter(Employee.employer_id == employer_id).count()
    total_emails = db.query(EmailSent).filter(EmailSent.employer_id == employer_id).count()
    total_clicks = (
        db.query(func.count(ClickEvent.id))
        .join(EmailSent, ClickEvent.email_id == EmailSent.id)
        .filter(EmailSent.employer_id == employer_id)
        .scalar()
    ) or 0

    return EmployerStatsOut(
        totalEmployees=total_employees,
        totalEmailsSent=total_emails,
        totalUrlsClicked=total_clicks,
    )
