from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from fastapi import Body
from models.admin.items import Item  # SQLAlchemy model
from config.db.session import get_db
from schemas.admin.items import ItemCreate, ItemOut , ItemUpdate # your Pydantic models
from schemas.admin.items import ItemAvailabilityUpdate  # ✅ This schema handles only is_available
from service.admin.item import update_item_availability
from service.admin.item import create_item_with_image , update_item, delete_item, get_items_by_category_id, get_items_by_category_and_availability, get_item_by_id , get_items_by_stall_id
from fastapi import Query, status
from typing import List



item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@item_router.post("/", response_model=ItemOut)
def create_item_api(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    Gst_precentage: Optional[float] = Form(0.0),
    tax_included: bool = Form(False),
    is_available: bool = Form(True),  # ✅ New field added here
    building_id: UUID = Form(...),
    stall_id: UUID = Form(...),
    category_id: UUID = Form(...),
    admin_id: Optional[str] = Form(None),
    manager_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Convert empty strings to None
    admin_id = admin_id or None
    manager_id = manager_id or None

    item_data = {
        "name": name,
        "description": description,
        "price": price,
        "Gst_precentage": Gst_precentage,
        "tax_included": tax_included,
        "is_available": is_available,  # ✅ Pass into schema
        "building_id": building_id,
        "stall_id": stall_id,
        "category_id": category_id,
        "admin_id": admin_id,
        "manager_id": manager_id
    }

    return create_item_with_image(
        db=db,
        item_data=ItemCreate(**item_data),
        file=file
    )

@item_router.put("/items/{item_id}", response_model=ItemOut)
def update_item_api(item_id: UUID, item_data: ItemUpdate, db: Session = Depends(get_db)):
    return update_item(item_id=item_id, item_data=item_data, db=db)

@item_router.delete("/items/{item_id}")
def delete_item_api(item_id: UUID, db: Session = Depends(get_db)):
    return delete_item(item_id, db)


@item_router.get("/items/category/{category_id}", response_model=list[ItemOut])
def fetch_items_by_category(category_id: UUID, db: Session = Depends(get_db)):
    return get_items_by_category_id(category_id, db)



@item_router.patch("/items/{item_id}/availability", response_model=ItemOut)
def update_item_availability_api(
    item_id: UUID,
    data: ItemAvailabilityUpdate = Body(...),
    db: Session = Depends(get_db)
):
    return update_item_availability(item_id=item_id, is_available=data.is_available, db=db)



@item_router.get("/items/category/{category_id}/availability", response_model=List[ItemOut])
def fetch_items_by_category_and_availability(
    category_id: UUID,
    is_available: bool = Query(..., description="Filter by availability (true/false)"),
    db: Session = Depends(get_db)
):
    return get_items_by_category_and_availability(category_id, is_available, db)



@item_router.get("/items/{item_id}", response_model=ItemOut)
def fetch_item_by_id(item_id: UUID, db: Session = Depends(get_db)):
    return get_item_by_id(item_id=item_id, db=db)


# service.admin.item.py
@item_router.get("/stall/{stall_id}", response_model=List[ItemOut])
def fetch_items_by_stall_id(stall_id: UUID, db: Session = Depends(get_db)):
    return get_items_by_stall_id(stall_id=stall_id, db=db)