import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.security_controller import SecurityController
from db.helpers import get_session
from db.models.securities import Token
from db.models.users import UserInfFromToken
from app.logger_project import init_logger
init_logger()

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    *,
    session: AsyncSession = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    logging.info(f"input_data: form_data.username={form_data.username}, form_data.password={form_data.password}")
    user: UserInfFromToken = await SecurityController.authenticate_user(
        form_data.username, form_data.password, session=session
    )

    if not user:
        logging.error("user not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await SecurityController.create_access_token(
        data={"sub": user.email, "username": user.username, "role": user.role}
    )
    logging.info(f"access_token={access_token}")

    return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/me", response_model=UserInfFromToken)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logging.info(f"input_data:token={token}")
    user: UserInfFromToken = await SecurityController.get_current_user(token)
    logging.info(f"user={user}")
    return user
