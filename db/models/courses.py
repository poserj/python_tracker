from typing import Optional

from sqlmodel import Field, SQLModel


class Courses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: int = Field(foreign_key="users.id")
    description: str


class Lessons(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: int = Field(foreign_key="users.id")
    conntext: str


class CoursesContexts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lessons.id")
    course_id: int = Field(foreign_key="courses.id")


class StudyCourses(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    course_id: int = Field(foreign_key="courses.id", primary_key=True)
    finished: Optional[bool] = False
    last_access_date: Optional[str] = None  # Optional[datetime] = None


class StudyLessons(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    lesson_id: int = Field(foreign_key="lessons.id", primary_key=True)
    status: bool
    last_access_date: str
