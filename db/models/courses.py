from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class BaseAccessDate(SQLModel):
    finished: Optional[bool] = Field(default=False)
    last_access_date: Optional[datetime] = Field(default=datetime.now())




class CoursesContext(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    course_id: int = Field(foreign_key="course.id")


class StudyCourse(BaseAccessDate, SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)



class StudyLesson(BaseAccessDate, SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id", primary_key=True)


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author_id: Optional[int] = Field(foreign_key="user.id", default=None)
    description: Optional[str]
    author: Optional['User'] = Relationship(back_populates="author_courses")
    users_of_course: list['User'] = Relationship(
        back_populates="user_courses", link_model=StudyCourse
    )


class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="user.id")
    conntext: str
    author: Optional['User'] = Relationship(back_populates="author_lessons")
    users_of_lessons: list['User'] = Relationship(
        back_populates="user_lessons", link_model=StudyLesson
    )