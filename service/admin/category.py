import uuid
import os
import shutil
from dotenv import load_dotenv
import boto3
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import io     
from PIL import Image  
from models.admin.category import Category
from models.admin.admin import Admin
from models.admin.manager import Manager
from models.admin.building import Building
from models.admin.stalls import Stall


load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION", "ap-south-1")


# ✅ Convert and Upload Image to S3 in WebP format
def upload_category_image_to_s3(file: UploadFile) -> str:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    s3 = session.client("s3")

    filename = f"{uuid.uuid4()}.webp"

    try:
        image = Image.open(file.file)
        webp_buffer = io.BytesIO()
        image.convert("RGB").save(webp_buffer, format="WEBP", quality=85)
        webp_buffer.seek(0)

        s3.upload_fileobj(
            webp_buffer,
            S3_BUCKET_NAME,
            filename,
            ExtraArgs={
                "ContentType": "image/webp"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload to S3 failed: {str(e)}")

    return f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"


# ✅ Create Category
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

    # Validation checks
    if admin_id and not db.query(Admin).filter(Admin.id == admin_id).first():
        raise HTTPException(status_code=404, detail="Admin not found")

    if manager_id and not db.query(Manager).filter(Manager.id == manager_id).first():
        raise HTTPException(status_code=404, detail="Manager not found")

    if not db.query(Building).filter(Building.id == building_id).first():
        raise HTTPException(status_code=404, detail="Building not found")

    if not db.query(Stall).filter(Stall.id == stall_id).first():
        raise HTTPException(status_code=404, detail="Stall not found")

    # ✅ Upload to S3 in WebP format
    image_url = upload_category_image_to_s3(file) if file else None

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
