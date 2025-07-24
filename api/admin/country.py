from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.admin.country import CountryCreate, CountryUpdate, CountryOut
from service.admin import country as country_service
from config.db.session import get_db
from api.admin.auth import get_current_admin  # ✅ Fixed import
from models.admin.admin import Admin

country_router = APIRouter(prefix="/admin/country", tags=["Country Selection"])


@country_router.post("/", response_model=CountryOut)
def create_country_selection(
    country_data: CountryCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return country_service.create_country_selection(db, country_data)


@country_router.get("/{admin_id}", response_model=CountryOut)
def get_country_selection(
    admin_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return country_service.get_country_by_admin(db, admin_id)


@country_router.put("/{admin_id}", response_model=CountryOut)
def update_country_selection(
    admin_id: str,
    update_data: CountryUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return country_service.update_country_selection(db, admin_id, update_data)


@country_router.delete("/{admin_id}")
def delete_country_selection(
    admin_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return country_service.delete_country_selection(db, admin_id)
