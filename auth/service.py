from sqlalchemy.orm import Session
from sqlalchemy import text

from auth.utils import verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str):
    sql = text("""
        SELECT 
            i.identity_id,
            i.password_hash,
            i.party_id,
            p.display_name,
            r.role_code
        FROM identities i
        JOIN parties p ON p.party_id = i.party_id
        LEFT JOIN party_role_assignments r ON r.party_id = p.party_id AND r.is_active = true
        WHERE i.provider = 'email' 
          AND i.provider_user_id = :email
    """)

    row = db.execute(sql, {"email": email}).fetchone()
    if not row:
        return None

    if not verify_password(password, row.password_hash):
        return None

    token = create_access_token({
        "identity_id": row.identity_id,
        "party_id": row.party_id,
        "role": row.role_code
    })

    return {
        "access_token": token,
        "party_id": row.party_id,
        "display_name": row.display_name,
        "role_code": row.role_code,
        "email": email
    }