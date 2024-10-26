from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserDB(UserAuth):
    hashed_password: str


class Token(BaseModel):
    token: str
    token_type: str



