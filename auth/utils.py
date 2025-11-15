from sqlalchemy import text
from sqlalchemy.orm import Session


def verify_password(db: Session, plain_password: str, hashed_password: str) -> bool:
    """
    Проверяем пароль через PostgreSQL pgcrypto:
    SELECT crypt('plain', hashed) = hashed
    """
    sql = text("SELECT crypt(:plain, :hashed) = :hashed AS match")
    result = db.execute(sql, {"plain": plain_password, "hashed": hashed_password}).scalar()
    return bool(result)