# app/crud.py

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from . import models
from .auth import get_password_hash

async def get_user_by_username(db: AsyncSession, username: str):
    statement = select(models.User).where(models.User.username == username)
    result = await db.execute(statement)
    return result.scalars().first()

async def create_user(db: AsyncSession, user: models.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    user_id = db_user.id
    
    db_account = models.Account(owner_id=user_id)
    db.add(db_account)
    await db.commit()
    
    final_user_statement = (
        select(models.User)
        .options(
            selectinload(models.User.account).selectinload(models.Account.transactions)
        )
        .where(models.User.id == user_id)
    )
    results = await db.execute(final_user_statement)
    return results.scalars().one()

async def create_transaction(db: AsyncSession, account_id: int, transaction: models.TransactionCreate, type: str):
    db_transaction = models.Transaction.model_validate(transaction, update={"type": type, "account_id": account_id})
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_account_by_user_id(db: AsyncSession, user_id: int):
    statement = select(models.Account).options(selectinload(models.Account.transactions)).where(models.Account.owner_id == user_id)
    result = await db.execute(statement)
    return result.scalars().first()

async def update_account_balance(db: AsyncSession, account: models.Account, new_balance: float):
    account.balance = new_balance
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account