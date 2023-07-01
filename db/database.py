from sqlmodel import create_engine, SQLModel

from models.users import User, Passwd, Users_roles
from models.courses import Lesson, Study_lesson, Course
from models.courses import Courses_context, Study_course

engine = create_engine('sqlite:///./data.db', echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
