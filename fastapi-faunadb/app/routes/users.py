import bcrypt
from utils import check_valid_id, JWT
from typing import List, Dict
from helpers import User, Tweet
from fastapi.routing import APIRouter
from fastapi import status, Request, Response, Header, HTTPException
from models import UserBase, UserRegister, UserSignIn, UpdateUserProfile

jwtUtils=JWT()
router = APIRouter()

async def authorize(bearer:str):
    if not bearer:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Token is required.'
        )
    if len(bearer.split(' ')) != 2 or bearer.split(' ')[0] != 'Bearer':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token is Invalid.'
        )
    token = bearer.split(' ')[-1]
    try:
        data = jwtUtils.decode_jwt(token)
        return data 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is Invalid or Expired.'
        )

@router.get('/users', response_model=Dict)
def get_all_users():
    """Get all users"""
    users = User().get_all_users()
    p = [user.pop('password') for user in users]
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No users found.'
        )
    return {
        'status':True,
        'message':f'Successfully fetched {len(users)} users.',
        'data':users
    }

@router.get('/user/{id}', response_model=Dict)
def get_user_by_id(id:str):
    """Get user by id"""
    if not check_valid_id(id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='User ID is invalid.'
        )
    
    user = User().get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This user does not exist.'
        )
    user['data'].pop('password')
    user['data']['tweets'] = Tweet().get_all_user_tweets(id)
    return {
        'status':True,
        'message':'User successfully fetched.',
        'data':user['data']
    }

@router.post('/user/register', response_model=Dict,status_code=status.HTTP_201_CREATED)
def register_user(user:UserRegister):
    """Register a new user"""
    if User().get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This user is already registered.'
        )
    user.password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    try:
        user = User().register_user(user.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e) or 'An unknown error occurred.'
        )
    user.pop('password')
    return {
        "status":True,
        "message":"User successfully registered.",
        "data":user
    }

@router.post('/user/login', response_model=Dict)
def login_user(user:UserSignIn):
    """Login a registered user."""
    user_data=User().get_user_by_email(user.email)
    if user_data and bcrypt.checkpw(
        user.password.encode('utf-8'),
        user_data['password'].encode('utf-8')):
        token = jwtUtils.generate_jwt(
            {'id':user_data['id'],'email':user_data['email'],'fullname':user_data['fullname'],'username':user_data['username']
        })
        user_data.pop('password')
        return {
            "status":True,
            "message":"User successfully Logged in.",
            "data":{
                **user_data,
                "access_token":token
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Email or Password'
        )

@router.get('/user', response_model=Dict)
async def get_user(Authorization: str=Header(None, description='Bearer token.')):
    user = await authorize(Authorization)
    return user

    

    

