from fastapi import FastAPI
# Esta importação agora aponta para nossa função de database adaptada para SQLModel
from .database import create_db_and_tables
from .routers import users, transactions

app = FastAPI(
    title="API Bancária com FastAPI e SQLModel", # Título atualizado para refletir a nova abordagem
    description="Projeto para gerenciar operações bancárias de depósitos, saques e extratos, com autenticação JWT.",
    version="2.0.0" # Versão atualizada
)

# A lógica do evento de startup é a mesma, mas agora cria as tabelas do SQLModel
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# A inclusão dos roteadores não muda nada
app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Bancária com SQLModel!"}