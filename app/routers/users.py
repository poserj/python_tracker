from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.helpers import get_session
from db.models.users import Role, User

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


@router.get("/lesson/{lesson_id}")
async def get_lesson_inf(lesson_id: Annotated[int, Path(gt=0)]):
    """информация об уроке"""
    return {"title": f"Lesson {lesson_id}", "message": "Theme of lesson"}


@router.get("/my_course/")
async def get_my_course():
    """информация о курсах юзера и прогресс"""
    return {"title": f"My courses", "message": "My courses progress"}


@router.post("/add_user/", status_code=status.HTTP_201_CREATED)
async def add_user(
    *, session: AsyncSession = Depends(get_session), user: User, role_id: int
):
    """add new user"""
    q_role_id = select(Role).filter(Role.id == role_id)
    fut_role_id = await session.execute(q_role_id)
    role: Role | None = fut_role_id.scalar()
    print(role)
    if role:
        user.roles = [role]
        session.add(user)
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="role not found"
        )
