from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.livro import Livro, Leitor, Emprestimo
from app.schemas import LivroSchema, LeitorSchema, EmprestimoSchema

router = APIRouter(prefix="/livros", tags=["Livros"])

# CRUD para Livros

@router.get("/")
def listar_livros(db: Session = Depends(get_db)):
    try:
        livros = db.query(Livro).all()
        return livros
    except SQLAlchemyError as e:
        db.rollback()  # Rollback em caso de erro no banco
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {str(e)}")

@router.post("/")
def criar_livro(livro: Livro, db: Session = Depends(get_db)):
    try:
        db.add(livro)
        db.commit()
        db.refresh(livro)
        return livro
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar livro: {str(e)}")

@router.get("/{livro_id}")
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    try:
        livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter livro: {str(e)}")

@router.put("/{livro_id}")
def atualizar_livro(livro_id: int, livro: Livro, db: Session = Depends(get_db)):
    try:
        db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if db_livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        for key, value in livro.dict(exclude_unset=True).items():
            setattr(db_livro, key, value)
        db.commit()
        db.refresh(db_livro)
        return db_livro
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar livro: {str(e)}")

@router.delete("/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    try:
        db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
        if db_livro is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        db.delete(db_livro)
        db.commit()
        return {"message": "Livro deletado com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar livro: {str(e)}")

@router.get("/livros/leitores/{leitor_id}")
def listar_livros_por_leitor(leitor_id: int, db: Session = Depends(get_db)):
    livros = db.query(Livro).join(Emprestimo).filter(Emprestimo.leitor_id == leitor_id).all()
    return livros

# CRUD para Leitores

@router.get("/leitores/")
def listar_leitores(db: Session = Depends(get_db)):
    try:
        return db.query(Leitor).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao listar leitores: {str(e)}")

@router.post("/leitores/")
def criar_leitor(leitor: LeitorSchema, db: Session = Depends(get_db)):
    try:
        db_leitor = Leitor(**leitor.dict())
        db.add(db_leitor)
        db.commit()
        db.refresh(db_leitor)
        return db_leitor
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar leitor: {str(e)}")

@router.get("/leitores/{leitor_id}")
def obter_leitor(leitor_id: int, db: Session = Depends(get_db)):
    try:
        leitor = db.query(Leitor).filter(Leitor.id == leitor_id).first()
        if leitor is None:
            raise HTTPException(status_code=404, detail="Leitor não encontrado")
        return leitor
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter leitor: {str(e)}")

@router.put("/leitores/{leitor_id}")
def atualizar_leitor(leitor_id: int, leitor: LeitorSchema, db: Session = Depends(get_db)):
    try:
        db_leitor = db.query(Leitor).filter(Leitor.id == leitor_id).first()
        if db_leitor is None:
            raise HTTPException(status_code=404, detail="Leitor não encontrado")
        for key, value in leitor.dict(exclude_unset=True).items():
            setattr(db_leitor, key, value)
        db.commit()
        db.refresh(db_leitor)
        return db_leitor
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar leitor: {str(e)}")

@router.delete("/leitores/{leitor_id}")
def deletar_leitor(leitor_id: int, db: Session = Depends(get_db)):
    try:
        db_leitor = db.query(Leitor).filter(Leitor.id == leitor_id).first()
        if db_leitor is None:
            raise HTTPException(status_code=404, detail="Leitor não encontrado")
        db.delete(db_leitor)
        db.commit()
        return {"message": "Leitor deletado com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar leitor: {str(e)}")

# CRUD para Emprestimos

@router.get("/emprestimos/")
def listar_emprestimos(db: Session = Depends(get_db)):
    try:
        return db.query(Emprestimo).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao listar empréstimos: {str(e)}")

@router.post("/emprestimos/")
def criar_emprestimo(emprestimo: EmprestimoSchema, db: Session = Depends(get_db)):
    try:
        db_emprestimo = Emprestimo(**emprestimo.dict())
        db.add(db_emprestimo)
        db.commit()
        db.refresh(db_emprestimo)
        return db_emprestimo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar empréstimo: {str(e)}")

@router.get("/emprestimos/{emprestimo_id}")
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    try:
        emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
        if emprestimo is None:
            raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
        return emprestimo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter empréstimo: {str(e)}")

@router.put("/emprestimos/{emprestimo_id}")
def atualizar_emprestimo(emprestimo_id: int, emprestimo: EmprestimoSchema, db: Session = Depends(get_db)):
    try:
        db_emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
        if db_emprestimo is None:
            raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
        for key, value in emprestimo.dict(exclude_unset=True).items():
            setattr(db_emprestimo, key, value)
        db.commit()
        db.refresh(db_emprestimo)
        return db_emprestimo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar empréstimo: {str(e)}")

@router.delete("/emprestimos/{emprestimo_id}")
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    try:
        db_emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
        if db_emprestimo is None:
            raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
        db.delete(db_emprestimo)
        db.commit()
        return {"message": "Empréstimo deletado com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar empréstimo: {str(e)}")
