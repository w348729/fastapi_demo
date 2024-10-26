from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import APIRouter
from jose import jwt, JWTError
from app.db.db_utils import db_demo


class UserAuth(BaseModel):
    username: str
    password: str


class UserDB(UserAuth):
    hashed_password: str


class Token(BaseModel):
    token: str
    token_type: str



