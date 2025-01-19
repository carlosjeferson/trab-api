from sqlmodel import create_engine, Session
from app.models.livro import SQLModel

DATABASE_URL = "sqlite:///./livros.db"  # Alterar para PostgreSQL se necessário

engine = create_engine(DATABASE_URL, echo=True)

def create_db():
    SQLModel.metadata.create_all(bind=engine)

def get_db():
    with Session(engine) as session:
        yield session
