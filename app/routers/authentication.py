import asyncio
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import BackgroundTasks
from datetime import datetime, timedelta
from fastapi import APIRouter
from jose import jwt, JWTError
from app.db.db_utils import db_demo
from app.models.user import UserAuth, UserDB


# just for demo example
SECRET_KEY = '12345678'  
ALGORITHM = 'HS256' 
ACCESS_TOKEN_EXPIRE_MINUTES = 300

auth_router = APIRouter(
    prefix='/auth'
)

user_collections = db_demo['users']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# verify with hashed password in db
def verify_password(user_password, input_password):
    return user_password == hash_password(input_password)


# to return a simple encode password
def hash_password(password: str):
    return f'r{password}'


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 


def auth_user(user_collections, username: str, password):
    user = get_user(user_collections, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = user_collections['username']
        return UserDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        print(1111111, token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_data = user_collections.find_one({'username': payload.get('username')})
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        return UserAuth(**user_data)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')


async def get_current_active_user(current_user: UserAuth = Depends(get_current_user)):
    return current_user


@auth_router.post('/register')
async def register_user(user: UserAuth, background_tasks: BackgroundTasks):
    if user_collections.find_one({'username': user.username}):
        raise HTTPException(status_code=400, detail='Username already exists.')
    hashed_password = hash_password(user.password)
    user_collections.insert_one({'username': user.username, 'password': hashed_password})
    return {'message': 'New User registered successfully.'}


@auth_router.post('/login')
async def login(user: UserAuth):
    user_data = user_collections.find_one({'username': user.username})
    if not user_data or verify_password(user.password, user_data['password']):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
 
    token = create_access_token(data={'username': user_data.get('username')})
    return {'access_token': token, 'token_type': 'bearer'}


@auth_router.get('/user_info')
async def read_users_me(current_user: UserAuth = Depends(get_current_active_user)):
    return current_user