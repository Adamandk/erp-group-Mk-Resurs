from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    party_id: str
    identity_id: str
    role_code: str
    my_company_id: str | None = None
    display_name: str