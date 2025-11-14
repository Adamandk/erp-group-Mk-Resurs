from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from db import get_db

app = FastAPI(
    title="ERP MK RESURS API",
    description="Backend для ERP (проекты, заявки, смены, финансы)",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "ERP MK RESURS backend is running",
    }


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    """
    Простой тест подключения к БД.
    Если всё норм — вернёт {"db": "ok"}.
    Если проблемы с Neon — здесь увидим ошибку в логах Railway.
    """
    db.execute(text("SELECT 1"))
    return {"db": "ok"}
