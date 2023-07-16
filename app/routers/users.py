from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import conlist, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.helpers import get_session
from db.models.courses import Course, StudyCourse
from db.models.users import Role, User, UsersRole

router = APIRouter()


@router.get("/app")
async def get_path_root(request: Request):
    return {"message": request.scope.get('root_path'), "title": "root"}


@router.get("/")
async def root():
    return {"message": "python_tracker app", "title": "python_tracker"}


@router.get("/courses")
async def get_courses():
    """информация о всех курсах"""
    return {"message": "All courses", "title": "Courses"}


@router.get("/course/{course_id}")
async def get_course_inf(course_id: Annotated[int, Path(gt=0)]):
    """информация о курсе"""
    return {"title": f"Course {course_id}", "message": "Themes"}


@router.patch("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_name(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: Annotated[int, Path(gt=0)],
    name: str):
    user: User = await session.get(User, user_id)
    setattr(user, 'name', name)
    session.add(user)
    await session.commit()



@router.get("/user/{user_id}")
async def get_user_inf(
    *, session: AsyncSession = Depends(get_session), user_id: Annotated[int, Path(gt=0)]
):
    """show information about user"""
    q_user = select(User).filter(User.id == user_id)
    fut_role_id = await session.execute(q_user)
    user: User | None = fut_role_id.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='user not found'
        )
    q_user_role = select(UsersRole).filter(UsersRole.user_id == user.id)
    fut_user_role = await session.execute(q_user_role)
    user_role: UsersRole = fut_user_role.scalar()
    q_role = select(Role).filter(Role.id == user_role.role_id)
    fut_role = await session.execute(q_role)
    role: Role = fut_role.scalar()

    q_user_course = select(StudyCourse).filter(StudyCourse.user_id == user.id)
    fut_user_course = await session.execute(q_user_course)
    study_courses: list[StudyCourse] | None = list(fut_user_course.scalars())
    user_courses_finished: list[Course] = []
    user_courses_study: list[Course] = []
    print("[study_courses", study_courses)
    if study_courses:
        for study_course in study_courses:
            print("[study_course  ", study_course)
            q_course = select(Course).filter(Course.id == study_course.course_id)
            fut_course = await session.execute(q_course)
            course: Course = fut_course.scalar()
            if study_course.finished:
                user_courses_finished.append(course)
            else:
                user_courses_study.append(course)

    return {
        "role": role.role,
        "email": user.email,
        "study courses": user_courses_study,
        "finished courses": user_courses_finished,
    }


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def add_user(
    *, session: AsyncSession = Depends(get_session), user: User, role_id: int
):
    """add new user"""
    q_role_id = select(Role).filter(Role.id == role_id)
    fut_role_id = await session.execute(q_role_id)
    role: Role | None = fut_role_id.scalar()
    if role:
        user.roles = [role]
        session.add(user)
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="role not found"
        )