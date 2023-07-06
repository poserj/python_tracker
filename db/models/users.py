from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from models.courses import StudyCourse


class BaseUser(SQLModel):
    created_on: datetime = Field(default=datetime.now())
    updated_on: datetime = Field(default=datetime.now())


class UsersRole(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )


class User(BaseUser, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    roles: list['Role'] = Relationship(back_populates='users', link_model=UsersRole)
    password: Optional['Passwd'] = Relationship(back_populates='user_pass')
    author_courses: list['Course'] = Relationship(back_populates="author")
    user_courses: list['Course'] = Relationship(back_populates='users_of_course', \
                                                link_model=StudyCourse)


class Passwd(BaseUser, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    passwd: str
    salt: str
    user_pass: Optional[User] = Relationship(back_populates='password')


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    users: list[User] = Relationship(back_populates='roles', link_model=UsersRole)
