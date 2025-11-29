# app/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str  # "employee" | "employer" | "developer"
    company_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    role: str

class EmployeeSummary(BaseModel):
    emails_received: int
    clicks: int

class EmployerSummary(BaseModel):
    total_emails: int
    total_clicks: int
    employee_count: int

class EmployeeItem(BaseModel):
    id: int
    name: str
    email: EmailStr
    clicks: int

class DevSummary(BaseModel):
    company_count: int
    employee_count: int
    total_clicks: int

class CompanyItem(BaseModel):
    id: int
    name: str
    employee_count: int
