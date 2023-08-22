from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.helpers import init_security
from app.services.user_controller import UserController

config = init_security()
print(config)
from db.models.users import UserInfFromToken, UserAdd, User, Role, Passwd

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password_from_db):
    return pwd_context.verify(plain_password, hashed_password_from_db)


def get_password_hash(password):
    return pwd_context.hash(password)


class SecurityController:
    @staticmethod
    async def authenticate_user(email, plain_password, session) -> UserInfFromToken:
        user_dict: dict = await UserController.get_user_inf_role_from_email(
            email=email, session=session
        )
        if not user_dict:
            return False
        password_from_db = user_dict["passwd"]  # ('igor', 'admin_1@example.com', 'administrator', 'password')
        if not verify_password(plain_password, password_from_db):
            return False
        user: UserInfFromToken = UserInfFromToken(username=user_dict["name"],\
                                                  email=user_dict["email"],\
                                                  role=user_dict["role"])
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
        print("====" * 30, expire)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
        )
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
            return UserInfFromToken(username=username, email=email, role=role)
        except JWTError:
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
            print(user)
            return True
        except:
            return False
