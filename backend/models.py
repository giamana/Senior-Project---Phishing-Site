from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

# -----------------------------
# Role Enum
# -----------------------------
class Role(str, enum.Enum):
    employee = "employee"
    employer = "employer"
    developer = "developer"

# -----------------------------
# User Model
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(120), nullable=False)   # ✅ added
    last_name = Column(String(120), nullable=True)     # ✅ added
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(Role), nullable=False)

    # If this user is an employer, they own one company
    company = relationship("Company", back_populates="employer", uselist=False)

# -----------------------------
# Company Model
# -----------------------------
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)

    employer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    employer = relationship("User", back_populates="company", foreign_keys=[employer_id])
    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")

# -----------------------------
# Employee Model
# -----------------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    company = relationship("Company", back_populates="employees")
    emails = relationship("EmailSent", back_populates="employee", cascade="all, delete-orphan")

# -----------------------------
# EmailTemplate Model
# -----------------------------
class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120), nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)

# -----------------------------
# EmailSent Model
# -----------------------------
class EmailSent(Base):
    __tablename__ = "emails_sent"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=True)

    unique_url_id = Column(String(64), unique=True, index=True, nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="emails")
    clicks = relationship("ClickEvent", back_populates="email", cascade="all, delete-orphan")

# -----------------------------
# ClickEvent Model
# -----------------------------
class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails_sent.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow)

    email = relationship("EmailSent", back_populates="clicks")
