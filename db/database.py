from sqlmodel import create_engine, SQLModel


from models.users import User, Passwd, Users_roles
from models.courses import Lesson, Study_lesson, Course
from models.courses import Courses_context, Study_course
from configs.helpers import init_db
db_conf = init_db()
engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
