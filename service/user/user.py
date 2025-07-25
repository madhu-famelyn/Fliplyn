# # services/user_service.py

# from sqlalchemy.orm import Session
# from models.user.user import User
# from schemas.user.user import UserSignup, OTPRequest, OTPVerify
# from service.otp_service import generate_otp, send_sms_otp
# from sqlalchemy.exc import IntegrityError
# from fastapi import HTTPException
# import logging

# logger = logging.getLogger(__name__)


# def create_user(db: Session, user_data: UserSignup) -> User:
#     print("📥 Incoming signup payload:", user_data)
#     """Creates a new user and generates an OTP"""
#     existing_user = db.query(User).filter(
#         (User.phone_number == user_data.phone_number) |
#         (User.company_email == user_data.company_email)
#     ).first()

#     if existing_user:
#         raise HTTPException(status_code=400, detail="User with this phone/email already exists.")

#     otp = generate_otp()

#     user = User(
#         name=user_data.name,
#         company_name=user_data.company_name,
#         company_email=user_data.company_email,
#         phone_number=user_data.phone_number,
#         otp=otp,
#         is_otp_verified=False
#     )

#     try:
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Failed to create user.")

#     send_sms_otp(user.phone_number, otp)
#     return user


# def send_otp(db: Session, req: OTPRequest) -> str:
#     """Resends OTP to phone or email"""
#     user = None
#     if req.phone_number:
#         user = db.query(User).filter(User.phone_number == req.phone_number).first()
#     elif req.company_email:
#         user = db.query(User).filter(User.company_email == req.company_email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found.")

#     otp = generate_otp()
#     user.otp = otp
#     db.commit()

#     if req.phone_number:
#         if not send_sms_otp(user.phone_number, otp):
#             raise HTTPException(status_code=500, detail="Failed to send SMS")

#     return otp


# def verify_otp(db: Session, data: OTPVerify) -> str:
#     """Verifies OTP for email or phone"""
#     user = None
#     if data.phone_number:
#         user = db.query(User).filter(User.phone_number == data.phone_number).first()
#     elif data.company_email:
#         user = db.query(User).filter(User.company_email == data.company_email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found.")

#     if user.otp != data.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     user.is_otp_verified = True
#     user.otp = None  # clear otp
#     db.commit()
#     return "OTP verified successfully."































from sqlalchemy.orm import Session
from models.user.user import User
from schemas.user.user import UserSignup, OTPRequest, OTPVerify, UserOut, UserUpdate
from service.otp_service import generate_otp, send_sms_otp, send_email_otp
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def create_user(db: Session, user_data: UserSignup) -> User:
    print("📥 Incoming signup payload:", user_data)
    """Creates a new user and generates an OTP"""
    existing_user = db.query(User).filter(
        (User.phone_number == user_data.phone_number) |
        (User.company_email == user_data.company_email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this phone/email already exists.")

    otp = generate_otp()

    user = User(
        name=user_data.name,
        company_name=user_data.company_name,
        company_email=user_data.company_email,
        phone_number=user_data.phone_number,
        otp=otp,
        is_otp_verified=False
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create user.")

    send_sms_otp(user.phone_number, otp)
    return user


def send_otp(db: Session, req: OTPRequest) -> str:
    user = None
    if req.phone_number:
        user = db.query(User).filter(User.phone_number == req.phone_number).first()
    elif req.company_email:
        user = db.query(User).filter(User.company_email == req.company_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    otp = generate_otp()
    user.otp = otp
    db.commit()

    if req.phone_number:
        if not send_sms_otp(user.phone_number, otp):
            raise HTTPException(status_code=500, detail="Failed to send SMS")
    elif req.company_email:
        if not send_email_otp(user.company_email, otp):
            raise HTTPException(status_code=500, detail="Failed to send Email")

    return otp


def verify_otp(db: Session, data: OTPVerify) -> str:
    """Verifies OTP for email or phone"""
    user = None
    if data.phone_number:
        user = db.query(User).filter(User.phone_number == data.phone_number).first()
    elif data.company_email:
        user = db.query(User).filter(User.company_email == data.company_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.is_otp_verified = True
    user.otp = None  # clear otp
    db.commit()
    return "OTP verified successfully."


def get_user_by_id(db: Session, user_id: str) -> UserOut:
    """Fetch user details by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user



def update_user(db: Session, user_id: str, user_update: UserUpdate) -> User:
    """Updates an existing user's details."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    try:
        if user_update.name is not None:
            user.name = user_update.name
        if user_update.company_name is not None:
            user.company_name = user_update.company_name
        if user_update.company_email is not None:
            user.company_email = user_update.company_email
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number

        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user.")


def delete_user(db: Session, user_id: str) -> str:
    """Deletes a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    try:
        db.delete(user)
        db.commit()
        return "User deleted successfully."
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete user.")
