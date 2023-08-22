import logging
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
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.security_controller import SecurityController
from app.services.user_controller import UserController
from db.helpers import get_session
from db.models.users import UserAdd
from app.logger_project import init_logger
init_logger()


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
    logging.info(f"input data: user_id={user_id}, name={name}")
    is_correct = await UserController.user_change_name(
        user_id=user_id, name=name, session=session
    )
    if not is_correct:
        logging.error("cant change name")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )


@usr_router.get("/{user_id}")
async def user_get_inf(
    *, session: AsyncSession = Depends(get_session), user_id: Annotated[int, Path(gt=0)]
):
    """show information about user"""
    logging.info(f"input data: user_id={user_id}")
    res: list = await UserController.get_user_inf_from_id(
        user_id=user_id, session=session
    )
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="information not found"
        )

    name, email, role, *_ = res[0]
    course_dict = UserController.get_filtered_course_from_status(res)
    logging.info(
        {
            "name": name,
            "role": role,
            "email": email,
            "study courses": course_dict.get("user_courses_study"),
            "finished courses": course_dict.get("user_courses_finished"),
        }
    )
    return {
        "name": name,
        "role": role,
        "email": email,
        "study courses": course_dict.get("user_courses_study"),
        "finished courses": course_dict.get("user_courses_finished"),
    }


@usr_router.post("/", status_code=status.HTTP_201_CREATED)
async def user_add(*, session: AsyncSession = Depends(get_session), user: UserAdd):
    """add new user"""
    logging.info(f"input data: user={user}")
    if not await SecurityController.user_add(user, session=session):
        logging.error("cant add user")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect data or email not unique",
        )


@usr_router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_change_role(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: Annotated[int, Path(gt=0)],
    role_id: Annotated[int, Query(gt=0)],
):
    """change role"""
    logging.info(f"input data: user_id={user_id}, role_id={role_id}")
    is_correct = await UserController.change_role(
        user_id=user_id, role_id=role_id, session=session
    )
    if not is_correct:
        logging.error("cant change role")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user or role not found"
        )
