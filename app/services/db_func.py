from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Request,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from db.models.courses import Course, StudyCourse
from db.models.users import Role, User, UserRole


async def _get_name_email_role_title_course_status_from_id(user_id: int, session: AsyncSession):
    q = select(User.name, User.email, Role.role, Course.title, StudyCourse.finished)
    q = q.join(UserRole, UserRole.user_id == User.id)
    q = q.join(Role, Role.id == UserRole.user_id)
    q = q.outerjoin(StudyCourse, StudyCourse.user_id == User.id)
    q = q.outerjoin(Course, Course.id == StudyCourse.course_id)
    q = q.where(User.id == user_id)
    res_future = await session.execute(q)
    res = res_future.all()
    if not res:
        return None
    else:
        return res


def _get_filtered_course_from_status(res: list)-> dict:
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
    print("lll"*7, course_dict)
    return course_dict

async def _user_add_from_user_role_id(user: User, role_id: int, session):
    role: Role | None = await session.get(Role, role_id)
    try:
        user.roles = [role]
        session.add(user)
        await session.commit()
        return True
    except:
        return False