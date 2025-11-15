from fastapi import FastAPI, Depends
from auth.router import router as auth_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from db import get_db

app = FastAPI(
    title="ERP MK RESURS API",
    description="Backend для ERP (проекты, заявки, смены, финансы)",
    version="0.1.0",
)

BASE_DIR = os.path.dirname(__file__)

app.include_router(auth_router, prefix="/auth")

# Раздача статических файлов (папка static)
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    """Отдаём файл static/index.html как простую HTML-страницу."""
    file_path = os.path.join(BASE_DIR, "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
        
@app.get("/ui/login", response_class=HTMLResponse)
def login_page():
    """Отдаём файл static/login.html (экран логина)."""
    file_path = os.path.join(BASE_DIR, "static", "login.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()