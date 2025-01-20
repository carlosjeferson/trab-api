from fastapi import FastAPI
from app.routes.livro_routes import router as livro_router
from app.core.config import init_db

app = FastAPI(
    title="API de Biblioteca",
    description="API para gerenciar livros, leitores e empréstimos.",
    version="1.0.0",
)

# Registrar as rotas
app.include_router(livro_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Livros"}
