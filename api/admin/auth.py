import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from dotenv import load_dotenv
from typing import Union
import os
import logging

from schemas.admin.token import TokenSchema
from models.admin.admin import Admin
from config.db.session import get_db

# ✅ Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# ✅ Logging for Render debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")

# ✅ Router
auth_router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


# ✅ Create Access Token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    if not SECRET_KEY:
        logger.error("JWT_SECRET_KEY not found in environment.")
        raise ValueError("JWT_SECRET_KEY is not set in the environment.")
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ✅ Admin Login Route (form data based)
@auth_router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        admin = db.query(Admin).filter(Admin.email == form_data.username).first()
        if not admin:
            logger.warning(f"Login failed: No admin found with email {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not bcrypt.verify(form_data.password, admin.hashed_password):
            logger.warning(f"Login failed: Incorrect password for {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(data={"sub": str(admin.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": admin.id,
                "email": admin.email,
                "name": admin.name
            }
        }
    except Exception as e:
        logger.exception("An unexpected error occurred during login.")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ Get current admin from token
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id = payload.get("sub")
        if not admin_id:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise credentials_exception

    return admin
