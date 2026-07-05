from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

Database_url = os.getenv("DATABASE_URL")

engine = create_engine(
    Database_url,
    pool_pre_ping=True,
    pool_recycle=180,
    pool_timeout=30,
    pool_size=5,
    max_overflow=10,
    echo=True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush= False
)

class Base(DeclarativeBase):
    pass
