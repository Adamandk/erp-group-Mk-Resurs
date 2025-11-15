from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from auth.schemas import LoginRequest, TokenResponse, UserInfo
from auth.service import authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": user["access_token"],
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserInfo)
def get_me(db: Session = Depends(get_db)):
    # позже добавим декодирование токена
    return {"detail": "Not implemented"}