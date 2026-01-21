from typing import Generator
from sqlmodel import create_engine, Session
from src.core.settings import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    Ensures proper session lifecycle management.
    """
    with Session(engine) as session:
        yield session
