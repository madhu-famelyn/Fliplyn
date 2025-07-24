from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.admin.admin import AdminCreate, AdminUpdate, AdminOut
from service.admin.admin import (
    create_admin,
    get_admin_by_id,
    update_admin,
    delete_admin,
)
from config.db.session import get_db

admin_router = APIRouter(prefix="/admin", tags=["Admin Users"])

# Create Admin
@admin_router.post("/", response_model=AdminOut)
def create_admin_user(admin_data: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(db, admin_data)

# Get Admin by ID
@admin_router.get("/{admin_id}", response_model=AdminOut)
def read_admin(admin_id: str, db: Session = Depends(get_db)):
    return get_admin_by_id(db, admin_id)

# Update Admin
@admin_router.put("/{admin_id}", response_model=AdminOut)
def update_admin_user(admin_id: str, update_data: AdminUpdate, db: Session = Depends(get_db)):
    return update_admin(db, admin_id, update_data)

# Delete Admin
 