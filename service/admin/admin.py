import re
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.admin.admin import Admin
from schemas.admin.admin import AdminCreate, AdminUpdate
from passlib.hash import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
PHONE_REGEX = re.compile(r'^\d{10}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$')

# Validation functions
def validate_email(email: str):
    if not EMAIL_REGEX.match(email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

def validate_phone(phone: str):
    if not PHONE_REGEX.match(phone):
        raise HTTPException(status_code=400, detail="Phone number must be 10 digits.")

def validate_password(password: str):
    if not PASSWORD_REGEX.match(password):
        raise HTTPException(
            status_code=400,
            detail="Password must be 8–12 characters with 1 uppercase, 1 digit, and 1 special character."
        )

# Hashing
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

# Create admin
def create_admin(db: Session, admin_data: AdminCreate):
    validate_email(admin_data.email)
    validate_phone(admin_data.phone_number)
    validate_password(admin_data.password)

    if db.query(Admin).filter(Admin.email == admin_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    if db.query(Admin).filter(Admin.phone_number == admin_data.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already registered.")

    new_admin = Admin(
        id=str(uuid.uuid4()),
        name=admin_data.name,
        email=admin_data.email,
        phone_number=admin_data.phone_number,
        hashed_password=hash_password(admin_data.password),
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

# Get admin by ID
def get_admin_by_id(db: Session, admin_id: str):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found.")
    return admin

# Update admin
def update_admin(db: Session, admin_id: str, update_data: AdminUpdate):
    admin = get_admin_by_id(db, admin_id)

    if update_data.email:
        validate_email(update_data.email)
        if update_data.email != admin.email and db.query(Admin).filter(Admin.email == update_data.email).first():
            raise HTTPException(status_code=400, detail="Email already in use.")
        admin.email = update_data.email

    if update_data.phone_number:
        validate_phone(update_data.phone_number)
        if update_data.phone_number != admin.phone_number and db.query(Admin).filter(Admin.phone_number == update_data.phone_number).first():
            raise HTTPException(status_code=400, detail="Phone number already in use.")
        admin.phone_number = update_data.phone_number

    if update_data.name:
        admin.name = update_data.name

    if update_data.password:
        validate_password(update_data.password)
        admin.hashed_password = hash_password(update_data.password)

    db.commit()
    db.refresh(admin)
    return admin

# Delete admin
def delete_admin(db: Session, admin_id: str):
    admin = get_admin_by_id(db, admin_id)
    db.delete(admin)
    db.commit()
    return {"detail": "Admin deleted successfully"}

