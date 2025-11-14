import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# В Railway мы потом зададим переменную окружения DATABASE_URL
# сюда надо будет вставить строку подключения от Neon.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Это сообщение ты увидишь в логах Railway, если забудешь настроить переменную
    raise RuntimeError("DATABASE_URL is not set. Please configure it in Railway env vars.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Зависимость для FastAPI: даёт сессию БД в запрос.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
