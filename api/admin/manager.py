from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.db.session import get_db
from schemas.admin.manager import ManagerCreate, ManagerUpdate, ManagerOut
from service.admin import manager as manager_service

manager_router = APIRouter(
    prefix="/managers",
    tags=["Managers"]
)

# ➕ Create Manager
@manager_router.post("/", response_model=ManagerOut, status_code=status.HTTP_201_CREATED)
def create_manager(manager_data: ManagerCreate, db: Session = Depends(get_db)):
    return manager_service.create_manager(db, manager_data)

# 📝 Update Manager
@manager_router.put("/{manager_id}", response_model=ManagerOut)
def update_manager(manager_id: str, manager_data: ManagerUpdate, db: Session = Depends(get_db)):
    return manager_service.update_manager(db, manager_id, manager_data)

# ❌ Delete Manager
@manager_router.delete("/{manager_id}", status_code=status.HTTP_200_OK)
def delete_manager(manager_id: str, db: Session = Depends(get_db)):
    return manager_service.delete_manager(db, manager_id)

# 📄 Get Managers by Building ID
@manager_router.get("/building/{building_id}", response_model=List[ManagerOut])
def get_managers_by_building(building_id: str, db: Session = Depends(get_db)):
    return manager_service.get_managers_by_building(db, building_id)

# 📄 Get Manager by Manager ID ✅ (new route)
@manager_router.get("/{manager_id}", response_model=ManagerOut)
def get_manager_by_id(manager_id: str, db: Session = Depends(get_db)):
    return manager_service.get_manager_by_id(db, manager_id)
