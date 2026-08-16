from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from collections.abc import Generator



class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()


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
