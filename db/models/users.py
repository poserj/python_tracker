from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseUser(SQLModel):
    created_on: datetime = Field(default=datetime.now())
    updated_on: datetime = Field(default=datetime.now())


class Users(BaseUser, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Passwds(BaseUser, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="users.id")
    passwd: str
    salt: str


class Roles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str


class UsersRoles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    roles_id: int = Field(default=None, foreign_key="roles.id")
