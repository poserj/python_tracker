from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "python_tracker app", "title": "python_tracker"}

