from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.admin.city import City
from schemas.admin.city import CityCreate, CityUpdate
from uuid import UUID
  
indian_cities = {
    "Hyderabad": "00001",
    "Mumbai": "00002",
    "Delhi": "00003",
    "Bengaluru": "00004",
    "Chennai": "00005",
    "Kolkata": "00006",
    "Pune": "00007",
    "Ahmedabad": "00008",
    "Jaipur": "00009",
    "Surat": "00010",
    "Lucknow": "00011",
    "Kanpur": "00012",
    "Nagpur": "00013",
    "Visakhapatnam": "00014",
    "Bhopal": "00015",
    "Patna": "00016",
    "Vadodara": "00017",
    "Ghaziabad": "00018",
    "Ludhiana": "00019",
    "Agra": "00020",
    "Nashik": "00021",
    "Faridabad": "00022",
    "Meerut": "00023",
    "Rajkot": "00024",
    "Kalyan-Dombivli": "00025",
    "Vasai-Virar": "00026",
    "Varanasi": "00027",
    "Srinagar": "00028",
    "Aurangabad": "00029",
    "Dhanbad": "00030",
    "Amritsar": "00031",
    "Navi Mumbai": "00032",
    "Allahabad": "00033",
    "Ranchi": "00034",
    "Howrah": "00035",
    "Coimbatore": "00036",
    "Jabalpur": "00037",
    "Gwalior": "00038",
    "Vijayawada": "00039",
    "Jodhpur": "00040",
    "Madurai": "00041",
    "Raipur": "00042",
    "Kota": "00043",
    "Guwahati": "00044",
    "Chandigarh": "00045",
    "Solapur": "00046",
    "Hubli–Dharwad": "00047",
    "Tiruchirappalli": "00048",
    "Bareilly": "00049",
    "Moradabad": "00050"
}

# ✅ Create a new city using city name to city_id mapping
def create_city(db: Session, city_data: CityCreate):
    city_id = indian_cities.get(city_data.city)
    if not city_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or unsupported city name: {city_data.city}"
        )

    new_city = City(
        admin_id=city_data.admin_id,
        country_id=city_data.country_id,
        state_id=city_data.state_id,
        city=city_data.city,
        city_id=city_id
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

# ✅ Get all cities
def get_all_cities(db: Session):
    return db.query(City).all()


# ✅ Get a single city by ID
def get_city_by_id(db: Session, city_id: UUID):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found"
        )
    return city


# ✅ Update a city by ID
def update_city(db: Session, city_id: UUID, city_update: CityUpdate):
    city = get_city_by_id(db, city_id)

    if city_update.city is not None:
        city.city = city_update.city
    if city_update.state_id is not None:
        city.state_id = city_update.state_id
    if city_update.country_id is not None:
        city.country_id = city_update.country_id

    db.commit()
    db.refresh(city)
    return city


# ✅ Delete a city by ID
def delete_city(db: Session, city_id: UUID):
    city = get_city_by_id(db, city_id)
    db.delete(city)
    db.commit()
    return {"detail": f"City with ID {city_id} deleted successfully"}
