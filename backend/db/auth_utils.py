# backend/db/auth_utils.py
import hashlib
import secrets

# Simple password hashing (use bcrypt/argon2 in production)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# In-memory session store (replace with DB-backed sessions for persistence)
SESSIONS = {}

def create_token(user_id: int) -> str:
    token = secrets.token_hex(32)
    SESSIONS[token] = {"user_id": user_id}
    return token

def invalidate_token(token: str):
    SESSIONS.pop(token, None)