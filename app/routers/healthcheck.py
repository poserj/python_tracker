from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "python_tracker app", "title": "python_tracker"}
