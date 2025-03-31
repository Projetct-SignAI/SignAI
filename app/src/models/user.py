from sqlalchemy.orm import Session
from src.utils.bancoPostgres import Base, engine
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Criar a tabela no banco de dados
Base.metadata.create_all(bind=engine)
