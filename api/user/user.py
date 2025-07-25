from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user.user import UserSignup, OTPRequest, OTPVerify, UserOut, UserUpdate
from service.user.user import create_user, send_otp, verify_otp, get_user_by_id, update_user, delete_user
from config.db.session import get_db

user_router = APIRouter()


@user_router.post("/signup", response_model=UserOut)
def register_user(user: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user and send OTP (via phone or email)
    """
    return create_user(db, user)


@user_router.post("/send-otp")
def resend_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """
    Resend OTP to phone or email (only one is required)
    """
    return {"message": f"OTP sent: {send_otp(db, request)}"}


@user_router.post("/verify-otp")
def verify_user_otp(data: OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP using phone or email
    """
    return {"message": verify_otp(db, data)}


@user_router.get("/user/{user_id}", response_model=UserOut)
def fetch_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Get user details by ID
    """
    return get_user_by_id(db, user_id)


@user_router.put("/user/{user_id}", response_model=UserOut)
def update_user_details(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user's details by ID
    """
    return update_user(db, user_id, user_update)



@user_router.delete("/user/{user_id}")
def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user by ID
    """
    return {"message": delete_user(db, user_id)}

