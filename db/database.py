from helpers import init_db
from models.courses import Courses, CoursesContexts, Lessons, StudyCourses, StudyLessons
from models.users import Passwds, Users, UsersRoles
from sqlmodel import SQLModel, create_engine

db_conf = init_db()
engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])


def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
