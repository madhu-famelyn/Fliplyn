from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from dotenv import dotenv_values
from config.db.session import get_db
from schemas.admin.manager import ManagerLogin, ManagerToken
from models.admin.manager import Manager

manager_login_router = APIRouter(prefix="/manager", tags=["Manager Auth"])

# ✅ Load environment variables
config = dotenv_values(".env")
SECRET_KEY = config.get("JWT_SECRET_KEY")
ALGORITHM = config.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# ✅ Token creation helper
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ POST /manager/login
@manager_login_router.post("/login", response_model=ManagerToken)
def login_manager(login_data: ManagerLogin, db: Session = Depends(get_db)):
    manager = db.query(Manager).filter(Manager.email == login_data.email).first()

    if not manager or not bcrypt.verify(login_data.password, manager.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": str(manager.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": manager.id,
            "email": manager.email
        }
    }
