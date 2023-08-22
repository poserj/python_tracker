from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from db.models.courses import Course, Lesson, StudyCourse, StudyLesson


class BaseUser(SQLModel):
    created_on: datetime = Field(default=datetime.now())
    updated_on: datetime = Field(default=datetime.now())


class UserInfFromToken(SQLModel, table=False):
    email: str | None = None
    username: str | None = None
    role: str | None = None

class UserAdd(SQLModel, table=False):
    email: str | None = None
    username: str | None = None
    role: int | None = None
    password: str | None = None



class UserRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")


class User(BaseUser, table=True):
    __table_args__ = ((UniqueConstraint('email', name='uc_user_email')),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    roles: list['Role'] = Relationship(back_populates='users', link_model=UserRole)
    password: Optional['Passwd'] = Relationship(back_populates='user_pass')
    author_courses: list[Course] = Relationship(back_populates="author")
    user_courses: list[Course] = Relationship(
        back_populates='users_of_course', link_model=StudyCourse
    )
    author_lessons: list[Lesson] = Relationship(back_populates="author")
    user_lessons: list[Lesson] = Relationship(
        back_populates='users_of_lessons', link_model=StudyLesson
    )


class Passwd(BaseUser, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    passwd: str
    salt: str
    user_pass: Optional[User] = Relationship(back_populates='password')


class Role(SQLModel, table=True):
    __table_args__ = ((UniqueConstraint('role', name='uc_role')),)
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    users: list[User] = Relationship(back_populates='roles', link_model=UserRole)
