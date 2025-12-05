from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from .models import User, Role, Company, Employee
from .schemas import SignupBody, LoginBody, UserOut, TokenOut

SECRET_KEY = "CHANGE_ME_SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
router = APIRouter()

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup", response_model=TokenOut)
def signup(body: SignupBody, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    normalized_role = Role(body.role.lower())
    user = User(
        first_name=body.first_name,
        last_name=body.last_name or "",
        email=body.email.lower(),
        role=normalized_role,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == Role.employer and body.companyName:
        company = Company(name=body.companyName, employer=user)
        db.add(company)
        db.commit()
        db.refresh(company)

    if user.role == Role.employee:
        emp = Employee(user_id=user.id, employer_id=None, company_id=None)
        db.add(emp)
        db.commit()
        db.refresh(emp)

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenOut(
        token=token,
        user=UserOut(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role.value,
            companyId=user.company.id if user.company else None,
            companyName=user.company.name if user.company else None,
        ),
    )

@router.post("/login", response_model=TokenOut)
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if pwd_context.needs_update(user.hashed_password):
        user.hashed_password = hash_password(body.password)
        db.add(user)
        db.commit()
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenOut(
        token=token,
        user=UserOut(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role.value,
            companyId=user.company.id if user.company else None,
            companyName=user.company.name if user.company else None,
        ),
    )
