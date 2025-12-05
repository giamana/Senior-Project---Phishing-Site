from typing import List
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User, Role
from .auth import SECRET_KEY, ALGORITHM  # reuse values from auth.py

# OAuth2PasswordBearer will automatically read the Authorization: Bearer <token> header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        role = payload.get("role")
        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def auth_required(user: User = Depends(get_current_user)) -> User:
    # This wrapper makes it easy to inject into routes
    return user

def require_role(user: User, allowed: List[Role]):
    if user.role not in allowed:
        raise HTTPException(status_code=403, detail="Forbidden for role")
