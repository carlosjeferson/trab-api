from pydantic import BaseModel
from typing import Optional
from datetime import date

class LivroBase(BaseModel):
    titulo: str
    autor: str
    edicao: str
    preco: float
    editora: Optional[str] = None
    ano: int
    genero: str

class LivroSchema(LivroBase):
    id: int

    class Config:
        orm_mode = True

class LeitorBase(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_nascimento: Optional[date] = None # Garante que a data é do tipo date

class LeitorSchema(LeitorBase):
    id: int

    class Config:
        orm_mode = True  # Necessário para conversão entre Pydantic e SQLModel

class EmprestimoBase(BaseModel):
    data_emprestimo: date
    data_devolucao: Optional[date] = None
    livro_id: int
    leitor_id: int

class EmprestimoSchema(EmprestimoBase):
    id: int

    class Config:
        orm_mode = True
