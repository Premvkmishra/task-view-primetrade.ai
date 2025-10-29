from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models import User, UserRole
from ...schemas import UserCreate, UserLogin, UserOut, AuthResponse
from ...security import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=payload.email,
        password=get_password_hash(payload.password),
        role=UserRole.user if payload.role is None else UserRole(payload.role),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"success": True, "data": {"user": UserOut.model_validate(user), "token": token}, "message": "Registered"}

@router.post("/login", response_model=AuthResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user: Optional[User] = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"success": True, "data": {"user": UserOut.model_validate(user), "token": token}, "message": "Logged in"}
