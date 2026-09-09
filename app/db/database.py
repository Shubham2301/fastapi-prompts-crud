from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from collections.abc import Generator


engine = create_engine(
    settings.database_url
)


SessionLocal = sessionmaker(
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
