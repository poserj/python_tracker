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

from db.helpers import get_session
from db.models.courses import Course, StudyCourse
from db.models.users import Role, User, UserRole

router = APIRouter()


@router.get("/app")
async def get_path_root(request: Request):
    return {"message": request.scope.get('root_path'), "title": "root"}


@router.get("/")
async def root():
    return {"message": "python_tracker app", "title": "python_tracker"}


@router.patch("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_name(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: Annotated[int, Path(gt=0)],
    name: Annotated[str, Body(min_length=4, max_length=15)],
):
    """change username"""
    user: User | None = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    setattr(user, 'name', name)
    session.add(user)
    await session.commit()


@router.get("/user/{user_id}")
async def get_user_inf(
    *, session: AsyncSession = Depends(get_session), user_id: Annotated[int, Path(gt=0)]
):
    """show information about user"""
    q = select(User.name, User.email, Role.role, Course.title, StudyCourse.finished)
    q = q.join(UserRole, UserRole.user_id == User.id)
    q = q.join(Role, Role.id == UserRole.user_id)
    q = q.outerjoin(StudyCourse, StudyCourse.user_id == User.id)
    q = q.outerjoin(Course, Course.id == StudyCourse.course_id)
    q = q.where(User.id == user_id)
    res_future = await session.execute(q)
    res = res_future.all()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="information not found"
        )
    name, email, role, *_ = res[0]
    user_courses_finished: list = []
    user_courses_study: list = []
    for _, _, _, st_course_title, st_course_finished in res:
        if st_course_finished:
            user_courses_finished.append(st_course_title)
        elif st_course_finished is not None:
            user_courses_study.append(st_course_title)
    return {
        "name": name,
        "role": role,
        "email": email,
        "study courses": user_courses_study,
        "finished courses": user_courses_finished,
    }


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def add_user(
    *, session: AsyncSession = Depends(get_session), user: User, role_id: int
):
    """add new user"""
    role: Role | None = await session.get(Role, role_id)
    if role:
        user.roles = [role]
        session.add(user)
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="role not found"
        )


@router.put("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_role(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: Annotated[int, Path(gt=0)],
    role_id: Annotated[int, Query(gt=0)],
):
    """change role"""
    q_user_role = select(UserRole).filter(UserRole.user_id == user_id)
    fut_user_role = await session.execute(q_user_role)
    user_role: UserRole = fut_user_role.scalar()
    user_role.role_id = role_id
    session.add(user_role)
    await session.commit()
