from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.db.session import get_db
from schemas.admin.state import StateCreate, StateUpdate, StateOut
from service.admin import state as state_service

state_router = APIRouter(prefix="/states", tags=["States"])


@state_router.post("/", response_model=StateOut)
def create_state(state_data: StateCreate, db: Session = Depends(get_db)):
    return state_service.create_state(db, state_data)


@state_router.get("/{state_id}", response_model=StateOut)
def get_state(state_id: str, db: Session = Depends(get_db)):
    state = state_service.get_state(db, state_id)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return state


@state_router.get("/", response_model=list[StateOut])
def get_all_states(db: Session = Depends(get_db)):
    return state_service.get_all_states(db)


@state_router.put("/{state_id}", response_model=StateOut)
def update_state(state_id: str, state_data: StateUpdate, db: Session = Depends(get_db)):
    updated_state = state_service.update_state(db, state_id, state_data)
    if not updated_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return updated_state


@state_router.delete("/{state_id}")
def delete_state(state_id: str, db: Session = Depends(get_db)):
    deleted_state = state_service.delete_state(db, state_id)
    if not deleted_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return {"message": "State deleted successfully"}
