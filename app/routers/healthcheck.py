from fastapi import APIRouter, Query, Path
from typing import Annotated


router = APIRouter()


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


