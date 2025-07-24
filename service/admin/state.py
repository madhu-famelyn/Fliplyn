from sqlalchemy.orm import Session
from models.admin.admin import Admin
from models.admin.state import State
from models.admin.country import CountrySelection
from schemas.admin.state import StateCreate, StateUpdate
from fastapi import HTTPException, status

# ✅ Fixed Indian state ID map
indian_states = {
    "Andhra Pradesh": "00001",
    "Arunachal Pradesh": "00002",
    "Assam": "00003",
    "Bihar": "00004",
    "Chhattisgarh": "00005",
    "Goa": "00006",
    "Gujarat": "00007",
    "Haryana": "00008",
    "Himachal Pradesh": "00009",
    "Jharkhand": "00010",
    "Karnataka": "00011",
    "Kerala": "00012",
    "Madhya Pradesh": "00013",
    "Maharashtra": "00014",
    "Manipur": "00015",
    "Meghalaya": "00016",
    "Mizoram": "00017",
    "Nagaland": "00018",
    "Odisha": "00019",
    "Punjab": "00020",
    "Rajasthan": "00021",
    "Sikkim": "00022",
    "Tamil Nadu": "00023",
    "Telangana": "00024",
    "Tripura": "00025",
    "Uttar Pradesh": "00026",
    "Uttarakhand": "00027",
    "West Bengal": "00028",
}


def create_state(db: Session, state_data: StateCreate):
    # ✅ Check if vendor exists
    vendor = db.query(Admin).filter(Admin.id == state_data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

    # ✅ Check if country exists
    country = db.query(CountrySelection).filter(CountrySelection.id == state_data.country_id).first()
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    # ✅ Get state_id from mapping
    state_id = indian_states.get(state_data.state_name)
    if not state_id:
        raise HTTPException(status_code=400, detail="Invalid state name provided")

    # ✅ Insert without uniqueness check
    new_state = State(
        vendor_id=state_data.vendor_id,
        country_id=state_data.country_id,
        state_name=state_data.state_name,
        state_id=state_id
    )

    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state




def get_state(db: Session, state_id: str):
    return db.query(State).filter(State.id == state_id).first()


def get_all_states(db: Session, skip: int = 0):  # Removed limit
    return db.query(State).offset(skip).all()


def update_state(db: Session, state_id: str, state_data: StateUpdate):
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        return None

    # If country_id is being updated, verify it exists
    if state_data.country_id:
        country = db.query(CountrySelection).filter(CountrySelection.id == state_data.country_id).first()
        if not country:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    for field, value in state_data.dict(exclude_unset=True).items():
        setattr(state, field, value)
    db.commit()
    db.refresh(state)
    return state


def delete_state(db: Session, state_id: str):
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        return None
    db.delete(state)
    db.commit()
    return state
