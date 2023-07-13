from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, Path, Request
from sqlmodel import create_engine, Session

from db.models.users import User, UsersRole, Role

router = APIRouter()
engine = create_engine('postgresql+psycopg2://user:pass@localhost:5432/app', echo=True)

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


@router.post("/add_user/", response_model=User)
async def add_user(user: User, role: int):
    """add new user"""
    with Session(engine) as session:
        role_id = session.query(Role).filter(Role.id == role).one()
        user.roles = [role_idma]
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

