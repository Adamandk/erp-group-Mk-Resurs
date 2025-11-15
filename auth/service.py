from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy import text
from sqlalchemy.orm import Session

from auth.utils import verify_password

SECRET_KEY = "MK_RESURS_SUPER_SECRET_KEY"  # можно потом вынести в env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def authenticate_user(db: Session, email: str, password: str):
    sql = text("""
        SELECT 
            i.identity_id,
            i.party_id,
            i.password_hash,
            pra.role_code
        FROM identities i
        LEFT JOIN party_role_assignments pra ON pra.party_id = i.party_id AND pra.is_active = true
        WHERE provider = 'email' AND provider_user_id = :email
        LIMIT 1
    """)

    row = db.execute(sql, {"email": email}).fetchone()
    if not row:
        return None

    identity_id, party_id, password_hash, role_code = row

    if not verify_password(db, password, password_hash):
        return None

    return {
        "identity_id": identity_id,
        "party_id": party_id,
        "role_code": role_code or "employee"
    }


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)