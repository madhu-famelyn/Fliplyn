import uuid
import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import boto3
# ✅ Upload Image to S3
from PIL import Image
import io


from models.admin.stalls import Stall
from models.admin.building import Building
from models.admin.admin import Admin
from models.admin.manager import Manager

load_dotenv()

# Load from .env
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION", "ap-south-1")




# ✅ Upload Image to S3 after converting to WebP
def upload_image_to_s3(file: UploadFile) -> str:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    s3 = session.client("s3")

    # Generate a WebP filename
    filename = f"{uuid.uuid4()}.webp"

    try:
        # ✅ Convert to WebP using Pillow
        image = Image.open(file.file)
        webp_buffer = io.BytesIO()
        image.convert("RGB").save(webp_buffer, format="WEBP", quality=85)
        webp_buffer.seek(0)

        # ✅ Upload WebP image
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

    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    if admin_id:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

    if manager_id:
        manager = db.query(Manager).filter(Manager.id == manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

    # ✅ Upload image to S3 if file exists
    image_url = upload_image_to_s3(file) if file else None

    new_stall = Stall(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        image_url=image_url,
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
