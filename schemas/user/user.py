from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


# ✅ Input schema for user signup (before OTP verification)
class UserSignup(BaseModel):
    name: str
    company_name: str
    company_email: EmailStr
    phone_number: constr(min_length=10, max_length=15)



# ✅ Schema to request OTP (via email or phone)
class OTPRequest(BaseModel):
    company_email: Optional[EmailStr] = None
    phone_number: Optional[constr(min_length=10, max_length=15)] = None

    def validate_input(self):
        if not self.company_email and not self.phone_number:
            raise ValueError("Either company_email or phone_number must be provided.")


# ✅ Schema for verifying OTP
class OTPVerify(BaseModel):
    otp: constr(min_length=4, max_length=8)
    company_email: Optional[EmailStr] = None
    phone_number: Optional[constr(min_length=10, max_length=15)] = None


# ✅ Output schema for user (after successful creation or fetch)
class UserOut(BaseModel):
    id: str
    name: str
    company_name: str
    company_email: EmailStr
    phone_number: str
    is_otp_verified: bool
    otp_verified_via: Optional[str] = None
    created_datetime: datetime

    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    phone_number: str


class LoginInitiate(BaseModel):
    phone_number: str | None = None
    company_email: EmailStr | None = None

class LoginVerify(BaseModel):
    phone_number: str | None = None
    company_email: EmailStr | None = None
    otp: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    company_email: Optional[EmailStr] = None
    phone_number: Optional[constr(min_length=10, max_length=15)] = None