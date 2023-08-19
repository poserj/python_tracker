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
from app.services.db_func import _get_name_email_role_title_course_status_from_id,\
    _get_filtered_course_from_status,\
    _user_add_from_user_role_id



usr_router = APIRouter()


@usr_router.get("/app")
async def get_path_root(request: Request):
    return {"message": request.scope.get('root_path'), "title": "root"}




@usr_router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_change_name(
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


@usr_router.get("/{user_id}")
async def user_get_inf(
    *, session: AsyncSession = Depends(get_session), user_id: Annotated[int, Path(gt=0)]
):
    """show information about user"""

    res: list = await _get_name_email_role_title_course_status_from_id(user_id=user_id, session=session)
    """
    res = [('igor', 'admin_1@example.com', 'administrator', 'Intro', True), \
    ('igor', 'admin_1@example.com', 'administrator', 'AsyncIO', True), \
    ('igor', 'admin_1@example.com', 'administrator', 'Course3', True), \
    ('igor', 'admin_1@example.com', 'administrator', 'Course4', False)]
    """
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="information not found"
        )

    name, email, role, *_ = res[0]
    course_dict = _get_filtered_course_from_status(res)
    return {
        "name": name,
        "role": role,
        "email": email,
        "study courses": course_dict.get("user_courses_study"),
        "finished courses": course_dict.get("user_courses_finished"),
    }


@usr_router.post("/", status_code=status.HTTP_201_CREATED)
async def user_add(
    *, session: AsyncSession = Depends(get_session),\
        user: User, role_id: int
):
    """add new user"""
    if not await _user_add_from_user_role_id(user, role_id, session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect data or email not unique"
        )




@usr_router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_change_role(
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


