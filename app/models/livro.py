from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date

class Livro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    autor: str
    edicao: str
    preco: float
    editora: Optional[str] = None
    ano: int
    genero: str

    emprestimos: List["Emprestimo"] = Relationship(back_populates="livro")

class Leitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_nascimento: Optional[date] = None

    emprestimos: List["Emprestimo"] = Relationship(back_populates="leitor")

class Emprestimo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_emprestimo: date
    data_devolucao: Optional[date] = None
    livro_id: int = Field(foreign_key="livro.id")
    leitor_id: int = Field(foreign_key="leitor.id")

    livro: Livro = Relationship(back_populates="emprestimos")
    leitor: Leitor = Relationship(back_populates="emprestimos")
