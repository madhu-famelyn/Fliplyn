from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from config.db.session import get_db
from schemas.admin.city import CityCreate, CityUpdate, CityOut
from service.admin import city as city_service

city_router = APIRouter(
    prefix="/cities",
    tags=["City Management"]
)

# ✅ Create a city
@city_router.post("/", response_model=CityOut, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return city_service.create_city(db, city)


# ✅ Get all cities
@city_router.get("/", response_model=List[CityOut])
def get_all_cities(db: Session = Depends(get_db)):
    return city_service.get_all_cities(db)


# ✅ Get a city by ID
@city_router.get("/{city_id}", response_model=CityOut)
def get_city_by_id(city_id: UUID, db: Session = Depends(get_db)):
    return city_service.get_city_by_id(db, city_id)


# ✅ Update a city
@city_router.put("/{city_id}", response_model=CityOut)
def update_city(city_id: UUID, city_data: CityUpdate, db: Session = Depends(get_db)):
    return city_service.update_city(db, city_id, city_data)


# ✅ Delete a city
@city_router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: UUID, db: Session = Depends(get_db)):
    city_service.delete_city(db, city_id)
    return {"detail": "City deleted successfully"}
