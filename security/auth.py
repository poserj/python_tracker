from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic.networks import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.helpers import get_session
from db.models.users import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    *, session: AsyncSession = Depends(get_session), \
        email: EmailStr, \
        passwd: str
):
    # user_q = select(User)
    # user_q = user_q.where(User.email == email)
    # res_future = await session.execute(user_q)
    # res = res_future.all()
    # print('cccc')
    user: User | None = await session.get(User, 1)


    # if not user:
    #     return False
    # if not verify_password(password, user.hashed_password):
    #     return False
    print('fff', user)
    return user
