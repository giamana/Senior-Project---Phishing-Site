# backend/routers/employees.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import auth_required, require_role
from ..models import User, Role, Employee, EmailSent, ClickEvent
from ..schemas import EmployeeRow, EmployerStatsOut  # use canonical schema name

router = APIRouter()

@router.get("/employee/{employee_user_id}/stats", response_model=EmployerStatsOut)
def employee_stats(employee_user_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    # employee can view own stats; employer/dev can view others
    if user.role == Role.employee and user.id != employee_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    emp = db.query(Employee).filter(Employee.user_id == employee_user_id).first()
    if not emp:
        return EmployerStatsOut(totalEmployees=0, totalEmailsSent=0, totalUrlsClicked=0)

    emails_sent = db.query(EmailSent).filter(EmailSent.employee_id == emp.id).count()
    urls_clicked = db.query(ClickEvent).filter(ClickEvent.employee_id == emp.id).count()

    return EmployerStatsOut(
        totalEmployees=1,  # this endpoint is per employee, so just 1
        totalEmailsSent=emails_sent,
        totalUrlsClicked=urls_clicked,
    )

@router.post("/employee/{employee_user_id}/add-id")
def employee_add_id(
    employee_user_id: int,
    employeeId: int = Body(..., embed=True),
    user: User = Depends(auth_required),
    db: Session = Depends(get_db),
):
    if user.id != employee_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    emp = db.get(Employee, employeeId)
    if not emp or emp.user_id != employee_user_id:
        raise HTTPException(status_code=400, detail="Invalid employeeId for this user")

    return {"linked": True, "employeeId": employeeId}

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    # Only Employer or Developer can delete employees
    
    require_role(user, [Role.employer, Role.developer])
    emp = db.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Employers can only delete their own employees
    if user.role == Role.employer and emp.employer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(emp)
    db.commit()
    return {"deleted": True, "employeeId": employee_id}


@router.post("/employee/{employee_user_id}/add-id")
def employee_add_id(employee_user_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    if user.id != employee_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    emp = db.query(Employee).filter(Employee.user_id == employee_user_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee record not found")

    return {"linked": True, "employeeId": emp.id}
