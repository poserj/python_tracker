from typing import Annotated

from fastapi import APIRouter, Path, Request
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models.users import Role, User, UsersRole
from db.helpers import init_db
config = init_db()
router = APIRouter()
engine = create_async_engine(config['DATABASE_URL'], echo=config['DEBUG_MOD'])


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


@router.post("/add_user/")#, response_model=User)
async def add_user(user: User, role: int):
    """add new user"""
    async with AsyncSession(engine) as session:
        #role_id = await session.query(Role).filter(Role.id == role).one()
        q_role_id = select(Role).filter(Role.id == role)
        role_id: int = await session.execute(q_role_id).results().one()
        print(role_id)
        # user.roles = [role_id]
        # await session.add(user)
        # await session.commit()
        # await session.refresh(user)
        # return user
