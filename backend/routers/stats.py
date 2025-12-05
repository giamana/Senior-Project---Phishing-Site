# backend/routers/stats.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import auth_required
from ..models import Employee, EmailSent, ClickEvent
from ..schemas import EmployerStatsOut

router = APIRouter()

@router.get("/stats/global", response_model=EmployerStatsOut)
def global_stats(authorization: str = Depends(auth_required), db: Session = Depends(get_db)):
    """
    Global stats endpoint returning totals that match EmployerStatsOut:
      - totalEmployees
      - totalEmailsSent
      - totalUrlsClicked
    Note: totalCompanies was removed from the response to match the schema.
    """
    total_employees = db.query(Employee).count()
    total_emails = db.query(EmailSent).count()
    total_clicks = db.query(ClickEvent).count()

    return EmployerStatsOut(
        totalEmployees=total_employees,
        totalEmailsSent=total_emails,
        totalUrlsClicked=total_clicks,
    )
