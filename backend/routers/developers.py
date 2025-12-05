# backend/routers/developers.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import auth_required, require_role
from ..models import User, Role, Company, Employee, EmailTemplate, EmailSent, ClickEvent
from ..schemas import CompanyRow, EmployerStatsOut, EmailCreate   # ✅ added EmailCreate
from ..services.email_service import send_email_to_employee

router = APIRouter()

@router.get("/companies")
def list_companies(authorization: str = Depends(auth_required), db: Session = Depends(get_db)):
    user: User = authorization
    companies = db.query(Company).all() if user.role == Role.developer else db.query(Company).filter(Company.employer_id == user.id).all()

    rows = []
    for c in companies:
        emp_list = db.query(Employee).filter(Employee.company_id == c.id).all()
        emp_ids = [e.id for e in emp_list]
        emails_sent = db.query(EmailSent).filter(EmailSent.employee_id.in_(emp_ids)).count() if emp_ids else 0
        urls_clicked = db.query(ClickEvent).filter(ClickEvent.employee_id.in_(emp_ids)).count() if emp_ids else 0
        rows.append({
            "id": c.id,
            "name": c.name,
            "employeesCount": len(emp_list),
            "emailsSent": emails_sent,
            "urlsClicked": urls_clicked,
            "employees": [
                {
                    "id": e.id,
                    "userId": e.user_id,
                    "first_name": db.get(User, e.user_id).first_name,
                    "last_name": db.get(User, e.user_id).last_name,
                    "emailsSent": db.query(EmailSent).filter(EmailSent.employee_id == e.id).count(),
                    "urlsClicked": db.query(ClickEvent).filter(ClickEvent.employee_id == e.id).count(),
                }
                for e in emp_list
            ],
        })
    return {"companies": rows}

@router.post("/developer/templates")
def create_template(
    name: str = Body(...),
    subject: str = Body(...),
    body: str = Body(...),
    authorization: str = Depends(auth_required),
    db: Session = Depends(get_db)
):
    user: User = authorization
    require_role(user, [Role.developer])
    template = EmailTemplate(developer_id=user.id, name=name, subject=subject, body=body)
    db.add(template)
    db.commit()
    db.refresh(template)
    return {"id": template.id, "name": template.name}

@router.post("/developer/send-email/{employee_id}")
def developer_send_email_with_template(
    employee_id: int,
    templateId: int = Body(..., embed=True),
    authorization: str = Depends(auth_required),
    db: Session = Depends(get_db)
):
    user: User = authorization
    require_role(user, [Role.developer])
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    template = db.get(EmailTemplate, templateId)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    track_url = send_email_to_employee(db, user, employee, template)
    return {"sent": True, "trackUrl": track_url}

@router.delete("/companies/{company_id}")
def delete_company(company_id: int, authorization: str = Depends(auth_required), db: Session = Depends(get_db)):
    user: User = authorization
    require_role(user, [Role.developer])
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"deleted": True, "companyId": company_id}

@router.get("/developer/employees")
def developer_list_employees(user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.developer])
    emps = db.query(Employee).all()
    rows = []
    for emp in emps:
        employee_user = db.get(User, emp.user_id)
        emails_sent = db.query(EmailSent).filter(EmailSent.employee_id == emp.id).count()
        urls_clicked = db.query(ClickEvent).filter(ClickEvent.employee_id == emp.id).count()
        rows.append({
            "id": emp.id,
            "userId": emp.user_id,
            "first_name": employee_user.first_name,
            "last_name": employee_user.last_name,
            "email": employee_user.email,
            "emailsSent": emails_sent,
            "urlsClicked": urls_clicked,
        })
    return {"employees": rows}

@router.post("/developer/send-email")
def developer_send_email_direct(body: EmailCreate, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.developer])
    emp = db.get(Employee, body.recipient_employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    track_url = send_email_to_employee(db, user, emp, body)
    return {"sent": True, "trackUrl": track_url}

@router.delete("/developer/delete-employee/{employee_id}")
def developer_delete_employee(employee_id: int, user: User = Depends(auth_required), db: Session = Depends(get_db)):
    require_role(user, [Role.developer])
    emp = db.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"deleted": True, "employeeId": employee_id}
