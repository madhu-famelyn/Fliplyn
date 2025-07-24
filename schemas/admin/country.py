from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CountryEnum(str, Enum):
    india = "India"
    kenya = "Kenya"
    usa = "USA"
    philippines = "Philippines"
    canada = "Canada"
    malaysia = "Malaysia"
    ksa = "KSA"
    bahrain = "Bahrain"
    nepal = "Nepal"
    ireland = "Ireland"
    nigeria = "Nigeria"
    finland = "Finland"
    china = "China"
    japan = "Japan"
    denmark = "Denmark"
    france = "France"
    south_korea = "South Korea"


class CountryCreate(BaseModel):
    admin_id: str = Field(..., example="uuid-of-admin")
    selected_country: CountryEnum = Field(..., example="India")


class CountryUpdate(BaseModel):
    selected_country: CountryEnum = Field(..., example="Canada")
class CountryOut(BaseModel):
    id: str
    admin_id: str
    selected_country: CountryEnum
    admin_name: str  # ✅ Add this field to match what you're returning

    class Config:
        from_attributes = True
    
