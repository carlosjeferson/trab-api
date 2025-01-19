from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./livros.db"  # Altere para PostgreSQL se necessário

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    SQLModel.metadata.create_all(engine)
