from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

Database_url = os.getenv("DATABASE_URL")

engine = create_engine(Database_url)

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush= False
)

class Base(DeclarativeBase):
    pass