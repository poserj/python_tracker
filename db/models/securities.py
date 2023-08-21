from sqlmodel import SQLModel


class Token(SQLModel, table=False):
    access_token: str
    token_type: str
