import logging
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.helpers import init_security
from app.services.user_controller import UserController

from db.models.users import Passwd, Role, User, UserAdd, UserInfFromToken
from app.logger_project import init_logger
init_logger()
config = init_security()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password_from_db):
    logging.info(f"{plain_password}, {hashed_password_from_db}")
    return pwd_context.verify(plain_password, hashed_password_from_db)


def get_password_hash(password):
    return pwd_context.hash(password)


class SecurityController:
    @staticmethod
    async def authenticate_user(email, plain_password, session) -> UserInfFromToken:
        logging.info(f"input data: email={email}, plain_password={plain_password}")
        user_dict: dict = await UserController.get_user_inf_role_from_email(
            email=email, session=session
        )
        if not user_dict:
            return False
        password_from_db = user_dict["passwd"]
        if not verify_password(plain_password, password_from_db):
            logging.info("Different passwords")
            return False
        user: UserInfFromToken = UserInfFromToken(
            username=user_dict["name"], email=user_dict["email"], role=user_dict["role"]
        )
        logging.info(user)
        return user

    @staticmethod
    async def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(
            minutes=config["ACCESS_TOKEN_EXPIRE_MINUTES"]
        ),
    ):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
        )
        logging.info(f"encoded_jwt={encoded_jwt}")
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str):
        try:
            payload = jwt.decode(
                token, config["SECRET_KEY"], algorithms=config["ALGORITHM"]
            )
            username: str = payload.get("username")
            role: str = payload.get("role")
            email: str = payload.get("sub")
            user_from_token = UserInfFromToken(username=username, email=email, role=role)
            logging.info(user_from_token)
            return user_from_token
        except JWTError:
            logging.error("Cant decode jwt")
            return False

    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    async def user_add(user_add: UserAdd, session):
        user = User(email=user_add.email, name=user_add.username)
        role: Role | None = await session.get(Role, user_add.role)
        try:
            user.roles = [role]
            hash_passwd = SecurityController.get_password_hash(user_add.password)
            password = Passwd(passwd=hash_passwd, salt="khgd56")
            user.password = [password]
            session.add(user)
            await session.commit()
            logging.info(user)
            return True
        except:
            logging.error("cant add user")
            return False
