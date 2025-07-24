from decimal import Decimal
from uuid import UUID
from models.admin.items import Item  # SQLAlchemy model
from schemas.admin.items import ItemCreate, ItemUpdate  # Pydantic model
from typing import List
from sqlalchemy.orm import Session
from fastapi import status

import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, Form
from typing import Optional
from models.admin.admin import Admin
from models.admin.manager import Manager
from models.admin.building import Building
from models.admin.stalls import Stall
from models.admin.category import Category

UPLOAD_DIR = "uploaded_images/items"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_item_image(file: UploadFile) -> str:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    file_ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save image")

    return file_path.replace("\\", "/")

def create_item_with_image(
    db: Session,
    item_data: ItemCreate,
    file: Optional[UploadFile] = None
):
    if not item_data.admin_id and not item_data.manager_id:
        raise HTTPException(status_code=400, detail="Either admin_id or manager_id must be provided.")

    base_price = Decimal(item_data.price)
    gst_percentage = Decimal(item_data.Gst_precentage or 0)

    # ✅ Calculate GST when tax_included=True
    if item_data.tax_included and gst_percentage > 0:
        final_price = base_price + (base_price * gst_percentage / 100)
    else:
        final_price = base_price

    image_url = save_item_image(file) if file else None

    item = Item(
        name=item_data.name,
        description=item_data.description,
        image_url=image_url,
        price=float(base_price),
        Gst_precentage=float(gst_percentage),
        final_price=float(final_price),
        tax_included=item_data.tax_included,
        building_id=item_data.building_id,
        stall_id=item_data.stall_id,
        category_id=item_data.category_id,
        admin_id=item_data.admin_id,
        manager_id=item_data.manager_id,
        is_available=item_data.is_available  # ✅ Included here
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_item(item_id: UUID, item_data: ItemUpdate, db: Session):
    # Convert UUID to string if DB stores item.id as VARCHAR
    item = db.query(Item).filter(Item.id == str(item_id)).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    # Update fields if provided
    update_fields = item_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(item, field, value)

    # Optionally recalculate final_price
    if "price" in update_fields or "Gst_precentage" in update_fields:
        price = update_fields.get("price", item.price)
        gst = update_fields.get("Gst_precentage", item.Gst_precentage or 0)
        item.final_price = price + (price * gst / 100)

    db.commit()
    db.refresh(item)
    return item

def delete_item(item_id: UUID, db: Session):
    item = db.query(Item).filter(Item.id == str(item_id)).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Item deleted successfully"}

def get_items_by_category_id(category_id: UUID, db: Session):
    items = db.query(Item).filter(Item.category_id == str(category_id)).all()
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found for this category"
        )
    return items


def update_item_availability(item_id: UUID, is_available: bool, db: Session):
    # Convert UUID to string if DB stores item.id as VARCHAR
    item = db.query(Item).filter(Item.id == str(item_id)).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item.is_available = is_available

    db.commit()
    db.refresh(item)
    return item



def get_items_by_category_and_availability(
    category_id: UUID, is_available: bool, db: Session
) -> List[Item]:
    items = db.query(Item).filter(
        Item.category_id == str(category_id),
        Item.is_available == is_available
    ).all()

    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found for this category with the specified availability"
        )

    return items

def get_item_by_id(item_id: UUID, db: Session) -> Item:
    item = db.query(Item).filter(Item.id == str(item_id)).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return item


def get_items_by_stall_id(stall_id: UUID, db: Session) -> List[Item]:
    items = db.query(Item).filter(Item.stall_id == str(stall_id)).all()
    
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found for this stall"
        )
    
    return items