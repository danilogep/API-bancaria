from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from datetime import datetime

# --- Modelos de Tabela (que também são Modelos Pydantic) ---

class TransactionBase(SQLModel):
    amount: float

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="transactions")

class AccountBase(SQLModel):
    balance: float = 0.0

class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="account")
    transactions: List[Transaction] = Relationship(back_populates="account")

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    account: Optional[Account] = Relationship(back_populates="owner")

# --- Esquemas Pydantic para a API (para entrada e saída de dados) ---

# Schema para criar um usuário (recebe a senha em texto plano)
class UserCreate(UserBase):
    password: str

# Schema para exibir a conta com suas transações
class AccountReadWithTransactions(AccountBase):
    id: int
    transactions: List[Transaction]

# Schema para exibir o usuário com sua conta
class UserReadWithAccount(UserBase):
    id: int
    account: Optional[AccountReadWithTransactions] = None

# Schema para criar uma transação
class TransactionCreate(TransactionBase):
    pass

# --- Esquemas para JWT ---
class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None

User.model_rebuild()
Account.model_rebuild()
Transaction.model_rebuild()