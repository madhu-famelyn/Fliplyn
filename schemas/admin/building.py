from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List, Union


# 👥 Manager Schema used inside BuildingCreate
class ManagerSchema(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john.doe@example.com")
    phone_number: Optional[str] = Field(None, example="9876543210")


# 🏢 Create Schema
class BuildingCreate(BaseModel):
    user_id: str = Field(..., example="uuid-of-admin")
    country_id: str = Field(..., example="uuid-of-country")
    state_id: str = Field(..., example="uuid-of-state")
    city_id: str = Field(..., example="uuid-of-city")
    building_name: str = Field(..., example="ABC Corporate Tower")
    user_access: Optional[Dict[str, Any]] = Field(
        None,
        example={"floor_access": [1, 2, 3], "entry_time": "9AM"}
    )
    managers: Optional[List[ManagerSchema]] = Field(
        default_factory=list,
        example=[
            {
                "name": "Manager One",
                "email": "one@example.com",
                "phone_number": "1234567890"
            },
            {
                "name": "Manager Two",
                "email": "two@example.com",
                "phone_number": "0987654321"
            }
        ]
    )


# ✏️ Update Schema
class BuildingUpdate(BaseModel):
    country_id: Optional[str] = Field(None, example="uuid-of-country")
    state_id: Optional[str] = Field(None, example="uuid-of-state")
    city_id: Optional[str] = Field(None, example="uuid-of-city")
    building_name: Optional[str] = Field(None, example="Updated Tower Name")
    user_access: Optional[Dict[str, Any]] = Field(
        None,
        example={"floor_access": [1, 2], "entry_time": "10AM"}
    )


# 👤 Manager Output for nested response
class ManagerOut(BaseModel):
    id: str
    name: str
    email: str
    phone_number: Optional[str]

    model_config = {
        "from_attributes": True
    }


# 🏢 Output Schema
class BuildingOut(BaseModel):
    id: str
    user_id: str
    country_id: str
    state_id: str
    city_id: str
    city_identifier: Optional[str]  # ✅ Required field
    building_name: str
    user_access: Optional[Dict[str, Any]]
    managers: List[ManagerOut] = []

    model_config = {
        "from_attributes": True
    }


# 🏢 Output with Location Names
class BuildingOutWithLocation(BaseModel):
    id: str
    user_id: str
    user_name: Optional[str]
    building_name: str

    country_id: str
    country_name: Optional[str]

    state_id: str
    state_name: Optional[str]

    city_id: str
    city_name: Optional[str]
    city_identifier: Optional[str] = None  # ✅ Fix: provide default

    user_access: Union[Dict[str, Any], None] = {}
    managers: List[ManagerOut]

    model_config = {
        "from_attributes": True
    }
