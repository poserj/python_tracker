from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.helpers import init_security
from app.services.user_controller import UserController

config = init_security()
print(config)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password_from_db):
    return True  # pwd_context.verify(plain_password, hashed_password_from_db)


def get_password_hash(password):
    return pwd_context.hash(password)


class SecurityController:
    @staticmethod
    async def authenticate_user(email, plain_password, session):
        user = await UserController.get_user_inf_role_from_email(
            email=email, session=session
        )
        password_from_db = plain_password  # make in the future
        if not user:
            return False
        if not verify_password(plain_password, password_from_db):
            return False
        return user
        # password make in the fututre

    @staticmethod
    async def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(
            minutes=config["ACCESS_TOKEN_EXPIRE_MINUTES"]
        ),
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        print("====" * 30, expire)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
        )
        return encoded_jwt
