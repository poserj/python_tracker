from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.security_controller import SecurityController
from db.helpers import get_session
from db.models.securities import Token
from db.models.users import User, UserInfFromToken

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    *,
    session: AsyncSession = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user: User = await SecurityController.authenticate_user(
        form_data.username, form_data.password, session=session
    )
    role = user[2]
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await SecurityController.create_access_token(
        data={"sub": user.email, "username": user.name, "role": role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/me", response_model=UserInfFromToken)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user: UserInfFromToken = await SecurityController.get_current_user(token)
    return user
