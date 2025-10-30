from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.post("/deposit", response_model=models.AccountReadWithTransactions, summary="Realiza um depósito na conta do usuário autenticado")
async def deposit(
    transaction: models.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Salvamos o ID imediatamente para evitar problemas com o objeto 'current_user' expirando.
    user_id = current_user.id

    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="O valor do depósito deve ser positivo")

    # Usamos a variável 'user_id' que é segura.
    account = await crud.get_account_by_user_id(db, user_id=user_id)
    new_balance = account.balance + transaction.amount

    await crud.create_transaction(db, account_id=account.id, transaction=transaction, type="deposit")
    await crud.update_account_balance(db, account=account, new_balance=new_balance)

    # Usamos a variável 'user_id' novamente para o retorno.
    return await crud.get_account_by_user_id(db, user_id=user_id)

@router.post("/withdraw", response_model=models.AccountReadWithTransactions, summary="Realiza um saque na conta do usuário autenticado")
async def withdraw(
    transaction: models.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    user_id = current_user.id

    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="O valor do saque deve ser positivo")

    account = await crud.get_account_by_user_id(db, user_id=user_id)

    if account.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    new_balance = account.balance - transaction.amount

    await crud.create_transaction(db, account_id=account.id, transaction=transaction, type="withdraw")
    await crud.update_account_balance(db, account=account, new_balance=new_balance)

    return await crud.get_account_by_user_id(db, user_id=user_id)

@router.get("/statement", response_model=models.AccountReadWithTransactions, summary="Exibe o extrato da conta do usuário autenticado")
async def get_statement(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    account = await crud.get_account_by_user_id(db, user_id=current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account