from typing import Optional

from sqlmodel import Field, SQLModel, Relationship





class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: int = Field(foreign_key="user.id")
    conntext: str


class CoursesContext(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    course_id: int = Field(foreign_key="course.id")


class StudyCourse(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)
    finished: Optional[bool] = False
    last_access_date: Optional[str] = None  # Optional[datetime] = None


class StudyLesson(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id", primary_key=True)
    status: bool
    last_access_date: str


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: int = Field(foreign_key="user.id")
    description: str
    author: Optional['User'] = Relationship(back_populates="author_courses")
    users_of_course: list['User'] = Relationship(back_populates="user_courses", \
                                               link_model=StudyCourse)