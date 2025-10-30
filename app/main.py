from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import users, transactions

app = FastAPI(
    title="API Bancária com FastAPI e SQLModel",
    description="Projeto para gerenciar operações bancárias de depósitos, saques e extratos, com autenticação JWT.",
    version="2.0.0"
)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Bancária com SQLModel!"}