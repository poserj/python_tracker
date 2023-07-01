import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_on: str#datetime
    updated_on: str#datetime

class Passwd(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, \
                              foreign_key="user.id")
    passwd: str
    created_on: str

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str

class Users_roles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    roles_id: int = Field(default=None, foreign_key="role.id")