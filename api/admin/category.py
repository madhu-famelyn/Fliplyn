from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from config.db.session import get_db
from schemas.admin.category import CategoryCreate, CategoryUpdate, CategoryOut
from service.admin import category as category_service

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.post("/", response_model=CategoryOut)
def create_category_api(
    name: str = Form(...),
    building_id: str = Form(...),
    stall_id: str = Form(...),
    admin_id: Optional[str] = Form(None),
    manager_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    return category_service.create_category(
        db=db,
        name=name,
        building_id=building_id,
        stall_id=stall_id,
        admin_id=admin_id,
        manager_id=manager_id,
        file=file
    )


@category_router.get("/", response_model=List[CategoryOut])
def get_all_categories_api(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)


@category_router.get("/{category_id}", response_model=CategoryOut)
def get_category_by_id_api(category_id: str, db: Session = Depends(get_db)):
    return category_service.get_category_by_id(db, category_id)


@category_router.get("/stall/{stall_id}", response_model=List[CategoryOut])
def get_categories_by_stall_api(stall_id: str, db: Session = Depends(get_db)):
    return category_service.get_categories_by_stall(db, stall_id)


@category_router.put("/{category_id}", response_model=CategoryOut)
def update_category_api(category_id: str, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(db, category_id, category_data)


@category_router.delete("/{category_id}")
def delete_category_api(category_id: str, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)
