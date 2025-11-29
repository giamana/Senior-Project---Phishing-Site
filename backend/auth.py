from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .schemas import SignupRequest, LoginRequest, TokenResponse, MessageResponse
from .models import User, Company
from .database import get_db

router = APIRouter()

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Config (use environment variables in production!)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ---------------- Password Helpers ----------------
def hash_password(password: str) -> str:
    # Ensure it's a string and truncate to 72 characters
    password_str = str(password)
    return pwd_context.hash(password_str[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_str = str(plain_password)
    return pwd_context.verify(plain_str[:72], hashed_password)


# ---------------- JWT Helpers ----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- Routes ----------------
@router.post("/signup", response_model=MessageResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(data.password)

    # Handle company creation/association
    company = None
    if data.company_name:
        existing_company = db.query(Company).filter(Company.name == data.company_name).first()
        if not existing_company:
            company = Company(name=data.company_name)
            db.add(company)
            db.flush()  # ensures company.id is available
        else:
            company = existing_company

    # Create user
    user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_pw,
        role=data.role,
        company_id=company.id if company else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully", "id": user.id, "role": user.role}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "role": user.role}
