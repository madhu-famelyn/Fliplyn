from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.db.session import get_db
from schemas.user.user import LoginInitiate, LoginVerify
from models.user.user import User
from service.user.auth import create_access_token
from service.otp_service import generate_otp, send_sms_otp

login_router = APIRouter(tags=["User Login"])


# ✅ Step 1: Send OTP (initiate login)
@login_router.post("/user/login/initiate")
def initiate_login(data: LoginInitiate, db: Session = Depends(get_db)):
    if not data.phone_number and not data.company_email:
        raise HTTPException(status_code=400, detail="Phone number or email is required")

    user = (
        db.query(User).filter(User.phone_number == data.phone_number).first()
        if data.phone_number else
        db.query(User).filter(User.company_email == data.company_email).first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Generate and save OTP
    otp = generate_otp()
    user.otp = otp
    db.commit()

    if data.phone_number:
        success = send_sms_otp(data.phone_number, otp)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
    else:
        print(f"[Mock Email] OTP for {data.company_email}: {otp}")  # Replace with email logic

    return {"message": "OTP sent successfully"}


# ✅ Step 2: Verify OTP and issue JWT
@login_router.post("/user/login/verify")
def verify_otp(data: LoginVerify, db: Session = Depends(get_db)):
    if not data.phone_number and not data.company_email:
        raise HTTPException(status_code=400, detail="Phone number or email is required")

    user = (
        db.query(User).filter(User.phone_number == data.phone_number).first()
        if data.phone_number else
        db.query(User).filter(User.company_email == data.company_email).first()
    )

    if not user or user.otp != data.otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    user.is_otp_verified = True
    user.otp = None
    db.commit()

    token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.company_email
        }
    }
