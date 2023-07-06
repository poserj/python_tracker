from helpers import init_db
from models.courses import Course, CoursesContext, Lesson, StudyCourse, StudyLesson
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
        # s = select(Role.id).where(Role.role == 'author')
        # role_autor = session.exec(s).one()
        n_adm = Role(role='super admin')
        # print('select', role_autor)
        passw = Passwd(passwd='111109876633', salt='ccddeffcc')
        # print('role', role_autor)
        vasy = User(name='igor Author', roles=[n_adm], password=[passw])
        course_history = Lesson(title='fastapi2', users_of_lessons=[vasy], conntext='2 attemp',  \
                                author=vasy)
        session.add(course_history)
        session.commit()
        session.refresh(course_history)
        print('after commit', vasy)
        print('after commit', course_history)
        # a = session.select(Users)
        # print(session.exec(a))


if __name__ == '__main__':
    create_tables()
    insert_test_data()
