from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from auth.schemas import LoginRequest, LoginResponse
from auth.service import authenticate_user, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({
        "identity_id": user["identity_id"],
        "party_id": user["party_id"],
        "role_code": user["role_code"],
    })

    return LoginResponse(
        access_token=token,
        party_id=user["party_id"],
        identity_id=user["identity_id"],
        role_code=user["role_code"],
    )