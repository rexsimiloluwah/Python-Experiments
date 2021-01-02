import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from config import engine, Session 
from utils import get_user_by_email, register_user, login_user, signJWT, decodeJWT
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from pydantic import ValidationError
from db.models import Base,BookStore,User
from schemas import UserBaseSchema,UserCreateSchema,UserLoginSchema,UserSchema,BookStoreSchema
from dependency import get_db 

router = APIRouter()

@router.post('/register', response_model = dict) 
def register(new_user: UserCreateSchema, db : Session = Depends(get_db)):
    print(new_user.email)
    user = get_user_by_email(db = db, user_email = new_user.email)
    if user:
        raise HTTPException(status_code = 400, detail = "User already registered, Please login.")
    else:
        try:
            register_user(db = db, user = new_user)
        except IntegrityError as err:
            raise HTTPException(status_code = 400, detail = "Please Enter all required fields.")
        except ValidationError as err:
            raise HTTPException(status_code = 400, detail = err)

        return {
            "message" : "Successfully registered a new user",
            "data" : new_user
        }

@router.post('/login', response_model = dict) 
def login(user: UserLoginSchema, db : Session = Depends(get_db)):
    try:
        return login_user(db = db, user = user)
    except ValidationError as err:
        raise HTTPException(status_code = 400, detail = err)

    


