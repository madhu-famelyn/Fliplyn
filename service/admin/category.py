import uuid
import os
import shutil
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from models.admin.category import Category
from models.admin.admin import Admin
from models.admin.manager import Manager
from models.admin.building import Building
from models.admin.stalls import Stall

# Make sure this directory exists
UPLOAD_DIR = "uploaded_images/categories"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_category_image(file: UploadFile) -> str:
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


def create_category(
    db: Session,
    name: str,
    building_id: str,
    stall_id: str,
    admin_id: str = None,
    manager_id: str = None,
    file: UploadFile = None
):
    if not admin_id and not manager_id:
        raise HTTPException(status_code=400, detail="Either admin_id or manager_id must be provided")

    # Validate relationships
    if admin_id and not db.query(Admin).filter(Admin.id == admin_id).first():
        raise HTTPException(status_code=404, detail="Admin not found")

    if manager_id and not db.query(Manager).filter(Manager.id == manager_id).first():
        raise HTTPException(status_code=404, detail="Manager not found")

    if not db.query(Building).filter(Building.id == building_id).first():
        raise HTTPException(status_code=404, detail="Building not found")

    if not db.query(Stall).filter(Stall.id == stall_id).first():
        raise HTTPException(status_code=404, detail="Stall not found")

    image_url = save_category_image(file) if file else None

    new_category = Category(
        id=str(uuid.uuid4()),
        name=name,
        image_url=image_url,
        building_id=building_id,
        stall_id=stall_id,
        admin_id=admin_id,
        manager_id=manager_id if manager_id else None,
    )
 
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_categories_by_stall(db: Session, stall_id: str):
    categories = db.query(Category).filter(Category.stall_id == stall_id).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found for the given stall")
    return categories


def update_category(db: Session, category_id: str, category_data):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_data.name is not None:
        category.name = category_data.name
    if category_data.image_url is not None:
        category.image_url = category_data.image_url
    if category_data.building_id is not None:
        category.building_id = category_data.building_id
    if category_data.stall_id is not None:
        category.stall_id = category_data.stall_id
    if category_data.admin_id is not None:
        category.admin_id = category_data.admin_id
    if category_data.manager_id is not None:
        category.manager_id = category_data.manager_id

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
