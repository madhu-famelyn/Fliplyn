import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from models.admin.manager import Manager
from models.admin.building import Building
from models.admin.admin import Admin
from schemas.admin.manager import ManagerCreate, ManagerUpdate


def create_manager(db: Session, manager_data: ManagerCreate):
    admin = db.query(Admin).filter(Admin.id == manager_data.admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    building = db.query(Building).filter(Building.id == manager_data.building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    if building.user_id != manager_data.admin_id:
        raise HTTPException(status_code=400, detail="Admin does not own the given building")

    existing = db.query(Manager).filter(
        (Manager.email == manager_data.email) | (Manager.phone_number == manager_data.phone_number)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Manager with given email or phone number already exists")

    new_manager = Manager(
        id=str(uuid.uuid4()),
        name=manager_data.name,
        email=manager_data.email,
        phone_number=manager_data.phone_number,
        password=bcrypt.hash(manager_data.password),  # ✅ Hashed password
        admin_id=manager_data.admin_id,
        building_id=manager_data.building_id
    )

    db.add(new_manager)

    user_access = building.user_access if isinstance(building.user_access, list) else []
    user_access.append({
        "id": new_manager.id,
        "name": new_manager.name,
        "email": new_manager.email,
        "phone_number": new_manager.phone_number
    })
    building.user_access = user_access

    db.commit()
    db.refresh(new_manager)

    return new_manager


def update_manager(db: Session, manager_id: str, manager_data: ManagerUpdate):
    manager = db.query(Manager).filter(Manager.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    if manager_data.name is not None:
        manager.name = manager_data.name
    if manager_data.email is not None:
        manager.email = manager_data.email
    if manager_data.phone_number is not None:
        manager.phone_number = manager_data.phone_number
    if manager_data.password is not None:
        manager.password = bcrypt.hash(manager_data.password)  # ✅ Update password if provided

    db.commit()
    db.refresh(manager)
    return manager


def delete_manager(db: Session, manager_id: str):
    manager = db.query(Manager).filter(Manager.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    building = db.query(Building).filter(Building.id == manager.building_id).first()
    if building and isinstance(building.user_access, list):
        # Remove manager from building.user_access
        building.user_access = [
            entry for entry in building.user_access
            if entry.get("id") != manager_id
        ]

    db.delete(manager)
    db.commit()
    return {"message": "Manager deleted successfully"}



def get_managers_by_building(db: Session, building_id: str):
    managers = db.query(Manager).filter(Manager.building_id == building_id).all()
    return managers


def get_manager_by_id(db: Session, manager_id: str):
    manager = db.query(Manager).filter(Manager.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager
