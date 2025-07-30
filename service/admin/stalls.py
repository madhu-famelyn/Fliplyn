import uuid
import os
import shutil
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from models.admin.stalls import Stall
from models.admin.building import Building
from models.admin.admin import Admin
from models.admin.manager import Manager


STALL_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "../../uploaded_images/stalls")
STALL_IMAGE_DIR = os.path.abspath(STALL_IMAGE_DIR)  # normalize to absolute path
os.makedirs(STALL_IMAGE_DIR, exist_ok=True)

def save_image_to_disk(file: UploadFile) -> str:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    file_ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(STALL_IMAGE_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

    # ✅ Return relative public path
    return f"/uploaded_images/stalls/{filename}"

def create_stall(
    db: Session,
    name: str,
    description: str,
    building_id: str,
    admin_id: str = None,
    manager_id: str = None,
    file: UploadFile = None
):
    admin_id = admin_id or None
    manager_id = manager_id or None

    if not admin_id and not manager_id:
        raise HTTPException(status_code=400, detail="Either admin_id or manager_id must be provided")

    # ✅ Validate building
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    # ✅ Validate admin (if provided)
    if admin_id:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

    # ✅ Validate manager (if provided)
    if manager_id:
        manager = db.query(Manager).filter(Manager.id == manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

    image_path = save_image_to_disk(file) if file else None

    new_stall = Stall(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        image_url=image_path,
        building_id=building_id,
        admin_id=admin_id,
        manager_id=manager_id
    )

    db.add(new_stall)
    db.commit()
    db.refresh(new_stall)
    return new_stall


def update_stall(db: Session, stall_id: str, stall_data):
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    if stall_data.name is not None:
        stall.name = stall_data.name
    if stall_data.description is not None:
        stall.description = stall_data.description
    if stall_data.image_url is not None:
        stall.image_url = stall_data.image_url
    if stall_data.admin_id is not None:
        stall.admin_id = stall_data.admin_id
    if stall_data.manager_id is not None:
        stall.manager_id = stall_data.manager_id

    db.commit()
    db.refresh(stall)
    return stall


def delete_stall(db: Session, stall_id: str):
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    db.delete(stall)
    db.commit()
    return {"message": "Stall deleted successfully"}


def get_stalls_by_building(db: Session, building_id: str):
    return db.query(Stall).filter(Stall.building_id == building_id).all()


def get_stall_by_id(db: Session, stall_id: str):
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")
    return stall
