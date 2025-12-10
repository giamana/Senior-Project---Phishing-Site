from typing import Optional
from pydantic import BaseModel, EmailStr

# ---------- Auth ----------
class SignupBody(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: Optional[str] = None
    role: str
    companyName: Optional[str] = None

class LoginBody(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    role: str
    companyId: Optional[int] = None
    companyName: Optional[str] = None

class TokenOut(BaseModel):
    token: str
    user: UserOut

# ---------- Employee / Employer ----------
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr

class EmployeeRow(BaseModel):
    id: int
    userId: int
    first_name: str
    last_name: Optional[str] = None
    emailsSent: int
    urlsClicked: int

class EmployerStatsOut(BaseModel):
    totalEmployees: int
    totalEmailsSent: int
    totalUrlsClicked: int

# ---------- Email ----------
class EmailCreate(BaseModel):
    subject: str
    body: str
    recipient_employee_id: int

# ---------- Company / Global ----------
class CompanyRow(BaseModel):
    id: int
    name: str
    employerId: Optional[int] = None

class GlobalStatsOut(BaseModel):
    totalCompanies: int
    totalEmployees: int
    totalEmailsSent: int
    totalUrlsClicked: int

# ---------- Compatibility aliases ----------
EmployeeStatsOut = EmployerStatsOut

