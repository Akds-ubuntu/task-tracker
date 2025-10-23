from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_db, create_access_token, get_current_user, revoke_all_token
from app.crud import get_user_by_email, create_user, authenticate_user, get_user_by_username
from app.schemas import UserOut, UserCreate, TokenOut, LoginRequest

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_email = get_user_by_email(db, user_in.email)
    existing_username = get_user_by_username(db, user_in.username)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    user = create_user(db, user_in.username, user_in.email, user_in.password)
    return user


@router.post("/login", response_model=TokenOut)
def login(user_in: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(db, user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    user, _ = current
    return user


@router.post("/logout")
def logout(current=Depends(get_current_user), db: Session = Depends(get_db)):
    user, jti = current
    revoke_all_token(db, user.id)
    return {"msg": "logged out"}
