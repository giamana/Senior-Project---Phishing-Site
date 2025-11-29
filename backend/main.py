from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from backend.models import (
    UserCreate,
    LoginRequest,
    TokenResponse,
    EmployeeSummary,
    EmployerSummary,
    DevSummary,
    EmployeeItem,
    CompanyItem,
)
from typing import List

app = FastAPI()

# ✅ Allow React frontend (localhost:5173) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust if frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Mock in-memory storage
USERS = {}       # email -> {password, name, role, company}
TOKENS = {}      # token -> {email, role}
EMPLOYEES = []   # [{id, name, email, clicks, company}]
COMPANIES = []   # [{id, name, employee_count}]
CAMPAIGNS = []   # [{id, employer_email, url, sent_to_emails}]


def verify_token(token: str = Depends(oauth2_scheme)):
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TOKENS[token]


# ✅ Signup
@app.post("/auth/signup", response_model=TokenResponse)
def signup(payload: UserCreate):
    if payload.email in USERS:
        raise HTTPException(status_code=400, detail="User already exists")
    USERS[payload.email] = {
        "password": payload.password,  # NOTE: hash in real app
        "name": payload.name,
        "role": payload.role,
        "company": payload.company_name,
    }
    token = f"token-{payload.email}"
    TOKENS[token] = {"email": payload.email, "role": payload.role}

    # Seed employee/company mock data
    if payload.role == "employee":
        EMPLOYEES.append({
            "id": len(EMPLOYEES) + 1,
            "name": payload.name,
            "email": payload.email,
            "clicks": 0,
            "company": payload.company_name,
        })

    if payload.company_name and not any(c["name"] == payload.company_name for c in COMPANIES):
        COMPANIES.append({
            "id": len(COMPANIES) + 1,
            "name": payload.company_name,
            "employee_count": 1,
        })

    return {"access_token": token, "role": payload.role}


# ✅ Login
@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = USERS.get(payload.email)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=422, detail="Invalid credentials")
    token = f"token-{payload.email}"
    TOKENS[token] = {"email": payload.email, "role": user["role"]}
    return {"access_token": token, "role": user["role"]}


# ✅ Employee Dashboard
@app.get("/employee/summary", response_model=EmployeeSummary)
def employee_summary(ctx=Depends(verify_token)):
    email = ctx["email"]
    emp = next((e for e in EMPLOYEES if e["email"] == email), None)
    if not emp:
        return {"emails_received": 0, "clicks": 0}
    emails_sent_to_emp = sum(1 for c in CAMPAIGNS if email in c.get("sent_to_emails", []))
    return {"emails_received": emails_sent_to_emp, "clicks": emp["clicks"]}


# ✅ Employer Dashboard
@app.get("/employer/summary", response_model=EmployerSummary)
def employer_summary(ctx=Depends(verify_token)):
    email = ctx["email"]
    role = ctx["role"]
    if role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")
    company = USERS[email]["company"]
    emp_in_company = [e for e in EMPLOYEES if e["company"] == company]
    total_emails = sum(len(c.get("sent_to_emails", [])) for c in CAMPAIGNS if USERS[c["employer_email"]]["company"] == company)
    total_clicks = sum(e["clicks"] for e in emp_in_company)
    return {
        "total_emails": total_emails,
        "total_clicks": total_clicks,
        "employee_count": len(emp_in_company),
    }


@app.get("/employer/employees", response_model=List[EmployeeItem])
def employer_employees(ctx=Depends(verify_token)):
    role = ctx["role"]
    if role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")
    company = USERS[ctx["email"]]["company"]
    emp_in_company = [e for e in EMPLOYEES if e["company"] == company]
    return emp_in_company


@app.post("/employer/campaigns")
def create_campaign(url: dict, ctx=Depends(verify_token)):
    role = ctx["role"]
    if role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")
    employer_email = ctx["email"]
    company = USERS[employer_email]["company"]
    recipients = [e["email"] for e in EMPLOYEES if e["company"] == company]
    CAMPAIGNS.append({
        "id": len(CAMPAIGNS) + 1,
        "employer_email": employer_email,
        "url": url.get("url"),
        "sent_to_emails": recipients,
    })
    return {"message": "Campaign created", "sent_to": recipients}


# ✅ Click Tracking
@app.get("/track/{campaign_id}/{employee_email}")
def track_click(campaign_id: int, employee_email: str):
    emp = next((e for e in EMPLOYEES if e["email"] == employee_email), None)
    if emp:
        emp["clicks"] += 1
    return {"message": "Click recorded"}


# ✅ Developer Dashboard
@app.get("/dev/summary", response_model=DevSummary)
def dev_summary(ctx=Depends(verify_token)):
    if ctx["role"] != "developer":
        raise HTTPException(status_code=403, detail="Forbidden")
    total_clicks = sum(e["clicks"] for e in EMPLOYEES)
    return {
        "company_count": len(COMPANIES),
        "employee_count": len(EMPLOYEES),
        "total_clicks": total_clicks,
    }


@app.get("/dev/companies", response_model=List[CompanyItem])
def dev_companies(ctx=Depends(verify_token)):
    if ctx["role"] != "developer":
        raise HTTPException(status_code=403, detail="Forbidden")
    return COMPANIES
