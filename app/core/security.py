from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.core.database import SessionLocal

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JWT = {
    'JWT_PRIVATE_KEY': settings.private_key_bytes,
    'JWT_PUBLIC_KEY': settings.public_key_bytes,
    'TIME_LIFE_ACCESS_TOKEN': settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    'ALGORITHM': settings.JWT_ALGORITHM,
}
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)


def create_access_token(db: Session, user_id: int) -> str:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    jti = str(uuid4())
    expire = datetime.utcnow() + timedelta(minutes=JWT['TIME_LIFE_ACCESS_TOKEN'])

    payload = {
        "sub": str(user_id),
        "jti": jti,
        "exp": expire,
        "version": user.token_version  # ← важное поле!
    }

    token = jwt.encode(payload, JWT['JWT_PRIVATE_KEY'], algorithm=JWT['ALGORITHM'])
    return token


def increment_token_version(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.token_version += 1
        db.commit()


def revoke_all_token(db: Session, user_id: int):
    increment_token_version(db, user_id)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT['JWT_PUBLIC_KEY'], algorithms=JWT['ALGORITHM'])
        user_id = int(payload.get("sub"))
        jti = payload.get("jti")
        token_version = payload.get("version")

        if user_id is None or jti is None or token_version is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.token_version != token_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    return user, jti
