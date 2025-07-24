import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.admin.country import CountrySelection
from schemas.admin.country import CountryCreate, CountryUpdate

def create_country_selection(db: Session, country_data: CountryCreate):
    # Check if an entry already exists for this admin
    existing = db.query(CountrySelection).filter_by(admin_id=country_data.admin_id).first()

    if existing:
        # ✅ Update the selected_country if it's different (or overwrite)
        existing.selected_country = country_data.selected_country
        db.commit()
        db.refresh(existing)

        return {
            "id": existing.id,
            "admin_id": existing.admin_id,
            "selected_country": existing.selected_country,
            "admin_name": existing.admin.name,  # ✅ Pull from relationship
        }

    # ✅ Create new
    country_entry = CountrySelection(
        id=str(uuid.uuid4()),
        admin_id=country_data.admin_id,
        selected_country=country_data.selected_country,
    )
    db.add(country_entry)
    db.commit()
    db.refresh(country_entry)

    return {
        "id": country_entry.id,
        "admin_id": country_entry.admin_id,
        "selected_country": country_entry.selected_country,
        "admin_name": country_entry.admin.name,  # ✅ Again, must come from relationship
    }



# ✅ Get country selection by admin ID
def get_country_by_admin(db: Session, admin_id: str):
    country = (
        db.query(CountrySelection)
        .filter_by(admin_id=admin_id)
        .join(CountrySelection.admin)
        .first()
    )
    if not country:
        raise HTTPException(status_code=404, detail="Country selection not found for this admin.")

    # Prepare dict manually to include admin name
    return {
        "id": country.id,
        "admin_id": country.admin_id,
        "selected_country": country.selected_country,
        "admin_name": country.admin.name  # ✅ Requires relationship to Admin model
    }



# ✅ Update country selection
def update_country_selection(db: Session, admin_id: str, update_data: CountryUpdate):
    country = db.query(CountrySelection).filter_by(admin_id=admin_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country selection not found.")

    country.selected_country = update_data.selected_country
    db.commit()
    db.refresh(country)
    return country


# ✅ Delete country selection
def delete_country_selection(db: Session, admin_id: str):
    country = db.query(CountrySelection).filter_by(admin_id=admin_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country selection not found.")

    db.delete(country)
    db.commit()
    return {"detail": "Country selection deleted successfully"}
