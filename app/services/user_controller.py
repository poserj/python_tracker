from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.courses import Course, StudyCourse
from db.models.users import Role, User, UserRole


class UserController:
    @staticmethod
    async def get_user_inf_from_id(user_id: int, session: AsyncSession):
        """get name, email, role, courses from user id"""
        q = (
            select(User.name, User.email, Role.role, Course.title, StudyCourse.finished)
            .join(UserRole, UserRole.user_id == User.id)
            .join(Role, Role.id == UserRole.role_id)
            .outerjoin(StudyCourse, StudyCourse.user_id == User.id)
            .outerjoin(Course, Course.id == StudyCourse.course_id)
            .where(User.id == user_id)
        )
        res_future = await session.execute(q)
        res = res_future.all()
        if not res:
            return None
        else:
            """
            res = [('igor', 'admin_1@example.com', 'administrator', 'Intro', True), \
            ('igor', 'admin_1@example.com', 'administrator', 'AsyncIO', True), \
            ('igor', 'admin_1@example.com', 'administrator', 'Course3', True), \
            ('igor', 'admin_1@example.com', 'administrator', 'Course4', False)]
            """
            return res

    @staticmethod
    async def get_user_inf_role_from_email(email: str, session: AsyncSession):
        """get name, email, role, courses from user id"""
        # user_q = select(User)
        # user_q = user_q.where(User.email == email)
        # res_future = await session.execute(user_q)
        # user: User = res_future.scalar()
        q = (
            select(User.name, User.email, Role.role)
            .join(UserRole, UserRole.user_id == User.id)
            .join(Role, Role.id == UserRole.role_id)
            .where(User.email == email)
        )
        res_future = await session.execute(q)
        res = res_future.one()
        """
        res = ('igor', 'admin_1@example.com', 'administrator')
        """
        if not res:
            return None
        else:
            return res

    @staticmethod
    def get_filtered_course_from_status(res: list) -> dict:
        course_dict = dict()
        user_courses_finished: list = []
        user_courses_study: list = []
        for _, _, _, st_course_title, st_course_finished in res:
            if st_course_finished:
                user_courses_finished.append(st_course_title)
            elif st_course_finished is not None:
                user_courses_study.append(st_course_title)
        course_dict["user_courses_finished"] = user_courses_finished
        course_dict["user_courses_study"] = user_courses_study
        return course_dict

    @staticmethod
    async def user_add(user: User, role_id: int, session):
        role: Role | None = await session.get(Role, role_id)
        try:
            user.roles = [role]
            session.add(user)
            await session.commit()
            return True
        except:
            return False

    @staticmethod
    async def user_change_name(user_id, name, session):
        user: User | None = await session.get(User, user_id)
        if not user:
            return False
        try:
            setattr(user, 'name', name)
            session.add(user)
            await session.commit()
            return True
        except:
            return False

    @staticmethod
    async def change_role(user_id, role_id, session):
        try:
            q_user_role = select(UserRole).filter(UserRole.user_id == user_id)
            fut_user_role = await session.execute(q_user_role)
            user_role: UserRole = fut_user_role.scalar()
            user_role.role_id = role_id
            session.add(user_role)
            await session.commit()
            return True
        except:
            return False
