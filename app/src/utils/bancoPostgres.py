from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


"""
DATABASE_URL = "postgresql+psycopg2://User:password@localhost:5432/SignAI"
"""

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/SignAI"


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()