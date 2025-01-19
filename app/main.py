from fastapi import FastAPI
from app.routes.livro_routes import router as livro_router
from app.core.config import init_db

app = FastAPI(title="Gerenciamento de Livros")

# Registrar as rotas
app.include_router(livro_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Livros"}
