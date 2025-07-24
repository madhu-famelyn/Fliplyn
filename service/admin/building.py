from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from models.admin.manager import Manager
from models.admin.category import Category
from models.admin.building import Building
from models.admin.admin import Admin
from models.admin.country import CountrySelection
from models.admin.items import Item  
from models.admin.state import State
from models.admin.city import City
from schemas.admin.building import BuildingCreate, BuildingUpdate, BuildingOutWithLocation, BuildingOut


def create_building(db: Session, building_data: BuildingCreate):
    # Validate admin user
    user = db.query(Admin).filter(Admin.id == building_data.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")

    # Validate country and state
    for model, value, name in [
        (CountrySelection, building_data.country_id, "Country"),
        (State, building_data.state_id, "State"),
    ]:
        if not db.query(model).filter(model.id == value).first():
            raise HTTPException(status_code=404, detail=f"{name} not found")

    # ✅ Fetch city and get city_id (e.g., "00001")
    city = db.query(City).filter(City.id == building_data.city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city_identifier = city.city_id  # <-- like "00002"

    # ✅ Create the building with city_identifier
    new_building = Building(
        id=str(uuid.uuid4()),
        user_id=building_data.user_id,
        country_id=building_data.country_id,
        state_id=building_data.state_id,
        city_id=building_data.city_id,
        building_name=building_data.building_name,
        user_access=building_data.user_access,
        city_identifier=city_identifier  # ✅ store it here
    )

    db.add(new_building)
    db.commit()
    db.refresh(new_building)

    # ✅ Create optional managers
    for manager_data in building_data.managers or []:
        existing = db.query(Admin).filter(Admin.email == manager_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Manager with email {manager_data.email} already exists")

        manager = Admin(
            id=str(uuid.uuid4()),
            name=manager_data.name,
            email=manager_data.email,
            phone_number=manager_data.phone_number,
            hashed_password=None  # You can improve this later
        )
        db.add(manager)

    db.commit()
    return new_building


def get_building(db: Session, building_id: str):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    # Convert to dictionary to safely handle dynamic fields
    building_dict = building.__dict__.copy()

    # 🛠️ Sanitize user_access
    user_access = building_dict.get("user_access")
    if not isinstance(user_access, dict):
        building_dict["user_access"] = {}

    # 🛠️ Pass managers as-is (Pydantic will serialize with from_attributes=True)
    building_dict["managers"] = building.managers

    return BuildingOut(**building_dict)



def get_buildings_by_admin_id(db: Session, admin_id: str):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")

    buildings_with_joins = (
        db.query(
            Building,
            CountrySelection.selected_country.label("country_name"),
            Admin.name.label("admin_name"),
            State.state_name.label("state_name"),
            City.city.label("city_name")
        )
        .join(CountrySelection, Building.country_id == CountrySelection.id)
        .join(Admin, Building.user_id == Admin.id)
        .outerjoin(State, Building.state_id == State.id)  # ✅ Join state
        .outerjoin(City, Building.city_id == City.id)     # ✅ Join city
        .filter(Building.user_id == admin_id)
        .all()
    )

    results = []
    for b, country_name, admin_name, state_name, city_name in buildings_with_joins:
        if b.user_access is not None and not isinstance(b.user_access, dict):
            b.user_access = {}

        results.append(
            BuildingOutWithLocation(
                id=b.id,
                user_id=b.user_id,
                user_name=admin_name,
                building_name=b.building_name,
                country_id=b.country_id,
                country_name=country_name,
                state_id=b.state_id,
                state_name=state_name,  # ✅ now set
                city_id=b.city_id,
                city_name=city_name,    # ✅ now set
                user_access=b.user_access,
                managers=b.managers,
            )
        )

    return results

def get_all_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Building).offset(skip).limit(limit).all()


def update_building(db: Session, building_id: str, building_data: BuildingUpdate):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    update_data = building_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(building, field, value)

    db.commit()
    db.refresh(building)
    return building


def delete_building(db: Session, building_id: str):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    # Step 1: Find all category IDs under this building
    category_ids = [cat.id for cat in db.query(Category.id).filter(Category.building_id == building_id).all()]

    # Step 2: Delete items under those categories
    if category_ids:
        db.query(Item).filter(Item.category_id.in_(category_ids)).delete(synchronize_session=False)

    # Step 3: Delete categories under the building
    db.query(Category).filter(Category.building_id == building_id).delete(synchronize_session=False)

    # Step 4: Delete managers under the building
    db.query(Manager).filter(Manager.building_id == building_id).delete(synchronize_session=False)

    # Step 5: Delete the building
    db.delete(building)

    db.commit()
    return building





def get_buildings_by_city_id(db: Session, city_id: str):
    buildings = (
        db.query(Building.id, Building.building_name)
        .filter(Building.city_id == city_id)
        .all()
    )

    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found for this city")

    return [{"id": b.id, "building_name": b.building_name} for b in buildings]


def get_buildings_by_city_identifier(db: Session, city_identifier: str):
    buildings = (
        db.query(Building.id, Building.building_name)
        .filter(Building.city_identifier == city_identifier)
        .all()
    )

    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found for this city identifier")

    return [{"id": b.id, "building_name": b.building_name} for b in buildings]
