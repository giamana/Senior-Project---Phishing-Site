from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List, Literal

class SignupRequest(BaseModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=100)
    email: EmailStr
    password: constr(min_length=6, max_length=72)
    role: Literal["employee", "employer", "developer"]
    company_name: Optional[constr(strip_whitespace=True, max_length=100)] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)

class TokenResponse(BaseModel):
    access_token: str
    role: Literal["employee", "employer", "developer"]

class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None
    role: Optional[str] = None

class SimulationCreate(BaseModel):
    subject: str
    content: str

class AssignRecipients(BaseModel):
    recipient_ids: List[int]
