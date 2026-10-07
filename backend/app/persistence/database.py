from collections.abc import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

SessionFactory = Callable[[], Session]

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
