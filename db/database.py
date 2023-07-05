from helpers import init_db
from models.courses import Courses, CoursesContexts, Lessons, StudyCourses, StudyLessons
from models.users import Passwd, User, UsersRole, Role
from sqlmodel import SQLModel, create_engine,  select, Session

db_conf = init_db()
engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])


def create_tables():
    SQLModel.metadata.create_all(engine)


def insert_test_data():
    with Session(engine) as session:
        n_adm = Role(role='super admin')
        passw = Passwd(passwd='111109876633', salt='ccddeffcc')
        print('role', n_adm)
        vasy = User(name='pety', roles=[n_adm], password=[passw])
        session.add(vasy)
        session.commit()
        session.refresh(vasy)
        print('vasy after commit', vasy)
        # a = session.select(Users)
        # print(session.exec(a))


if __name__ == '__main__':
    create_tables()
    insert_test_data()
