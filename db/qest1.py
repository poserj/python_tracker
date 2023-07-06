from helpers import init_db
from models.courses import Courses, CoursesContexts, Lessons, StudyCourses, StudyLessons
from models.users import Passwd, Role, User, UsersRole
from sqlmodel import Session, SQLModel, create_engine, select


def create_tables():
    db_conf = init_db()
    engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])
    SQLModel.metadata.create_all(engine)


def insert_test_data():
    db_conf = init_db()
    engine = create_engine(db_conf['DATABASE_URL'], echo=db_conf['DEBUG_MOD'])
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
