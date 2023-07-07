from helpers import init_db
from models.courses import Course, CoursesContext, Lesson, StudyCourse, StudyLesson
from models.users import Passwd, Role, User, UsersRole
from sqlmodel import Session, SQLModel, create_engine, select


def create_tables():
    engine = create_engine('sqlite:///./data.db', echo=True)
    SQLModel.metadata.create_all(engine)


def insert_test_data():
    engine = create_engine('sqlite:///./data.db', echo=True)
    # with Session(engine) as session:
    # n_adm = Role(role='super admin')
    # passw = Passwd(passwd='111109876633', salt='ccddeffcc')
    # print('role', n_adm)
    # vasy = User(name='pety', roles=[n_adm], password=[passw])
    # # session.add(vasy)
    # # session.commit()
    # session.refresh(vasy)
    # print('vasy after commit', vasy)

    with Session(engine) as session:
        passw = Passwd(passwd='111109876633', salt='ccddeffcc')
        vasy = User(name='pety', role=[1], password=passw)
        # vasy = User(name='pety', role=[1], password=[passw])

        session.add(vasy)
        session.commit()
        session.refresh(vasy)
        print('vasy after commit', vasy)


if __name__ == '__main__':
    create_tables()
    insert_test_data()