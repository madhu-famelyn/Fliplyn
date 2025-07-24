from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from schemas.admin.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingOut,
    BuildingOutWithLocation
)
from service.admin import building as building_service  # ✅ Import service
from config.db.session import get_db

building_router = APIRouter(prefix="/buildings", tags=["Buildings"])


@building_router.post("/", response_model=BuildingOut, status_code=status.HTTP_201_CREATED)
def create_building(building_data: BuildingCreate, db: Session = Depends(get_db)):
    return building_service.create_building(db, building_data)


@building_router.get("/{building_id}", response_model=BuildingOut)
def get_building(building_id: str, db: Session = Depends(get_db)):
    return building_service.get_building(db, building_id)


@building_router.get("/buildings/by-admin/{admin_id}", response_model=List[BuildingOutWithLocation])
def get_buildings_for_admin(admin_id: str, db: Session = Depends(get_db)):
    return building_service.get_buildings_by_admin_id(db, admin_id)


@building_router.get("/", response_model=List[BuildingOut])
def get_all_buildings(skip: int = 0, db: Session = Depends(get_db)):
    return building_service.get_all_buildings(db, skip)


@building_router.put("/{building_id}", response_model=BuildingOut)
def update_building(building_id: str, building_data: BuildingUpdate, db: Session = Depends(get_db)):
    return building_service.update_building(db, building_id, building_data)


@building_router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(building_id: str, db: Session = Depends(get_db)):
    building_service.delete_building(db, building_id)
    return {"detail": "Building deleted successfully"}


@building_router.get("/by-city/{city_id}", response_model=List[Dict[str, str]])
def list_buildings_by_city(city_id: str, db: Session = Depends(get_db)):
    return building_service.get_buildings_by_city_id(db, city_id)


# ✅ FIXED: use correct service function
@building_router.get("/by-city-identifier/{city_identifier}")
def get_buildings_by_identifier(city_identifier: str, db: Session = Depends(get_db)):
    return building_service.get_buildings_by_city_identifier(db, city_identifier)
