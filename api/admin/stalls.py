from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.admin.stalls import StallUpdate, StallOut
from service.admin.stalls import (
    create_stall,
    get_stall_by_id,
    get_stalls_by_building,
    update_stall,
    delete_stall,
)
from config.db.session import get_db

stall_router = APIRouter(prefix="/stalls", tags=["Stalls"])


@stall_router.post("/", response_model=StallOut)
async def create_stall_api(
    name: str = Form(...),
    description: str = Form(...),
    building_id: str = Form(...),
    admin_id: Optional[str] = Form(None),
    manager_id: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
# ✅ Correct
    return create_stall(
        db=db,
        name=name,
        description=description,
        building_id=building_id,
        admin_id=admin_id,
        manager_id=manager_id,
        file=file
    )



@stall_router.get("/{stall_id}", response_model=StallOut)
def get_stall_by_id_api(stall_id: str, db: Session = Depends(get_db)):
    return get_stall_by_id(db, stall_id)


@stall_router.get("/building/{building_id}", response_model=List[StallOut])
def get_stalls_by_building_api(building_id: str, db: Session = Depends(get_db)):
    return get_stalls_by_building(db, building_id)


@stall_router.put("/{stall_id}", response_model=StallOut)
def update_stall_api(stall_id: str, stall_data: StallUpdate, db: Session = Depends(get_db)):
    return update_stall(db, stall_id, stall_data)


@stall_router.delete("/{stall_id}")
def delete_stall_api(stall_id: str, db: Session = Depends(get_db)):
    return delete_stall(db, stall_id)
