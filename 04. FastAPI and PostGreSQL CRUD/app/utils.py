from sqlalchemy.orm import Session
from config import JWT_SECRET, JWT_ALGORITHM 
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import json
import bcrypt
import jwt 
import datetime, time
from db.models import (
    Base,
    BookStore,
    User
)

from schemas import (
    UserBaseSchema,
    UserCreateSchema,
    UserLoginSchema,
    UserSchema,
    BookStoreSchema
)

bcrypt_salt = bcrypt.gensalt()

def signJWT(user : UserSchema, response_model = dict):
    payload = {
        **user,
        "expires" :  time.time() + 3600 # Token expires in 1 hour
        # datetime.datetime.utcnow() + datetime.timedelta(hours = 1)
    }
    # print(payload)

    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return {
        "access_token" : token
    }

def decodeJWT(token : str, response_model = dict):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms= [JWT_ALGORITHM])
        print(decoded)
        if int(decoded["expires"]) > int(time.time()):
            return decoded 
        raise HTTPException(status_code = 400, detail = "Invalid or Expired Token")
    except:
        raise HTTPException(status_code = 400, detail = "Invalid or Expired Token")
    
def get_user_by_id(db : Session, user_id : int):
    return db.query(User).filter(
        User.id == user_id
    ).first()

def get_user_by_email(db : Session, user_email : str):
    return db.query(User).filter(
        User.email == user_email
    ).first()

def register_user(db : Session, user : UserCreateSchema):
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt_salt)
    new_user = User(
        firstname = user.firstname, lastname = user.lastname,
        email = user.email, password = user.password.decode()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

def login_user(db : Session, user : UserLoginSchema, response_model = dict):
    user_exists = get_user_by_email(db = db, user_email = user.email)
    asdict = lambda x: {c.name: str(getattr(x, c.name)) for c in x.__table__.columns}
    if not user_exists:
        raise HTTPException(status_code = 400, detail = "User is not registered in the database.")
    password_correct = bcrypt.checkpw(user.password.encode('utf-8'), user_exists.password.encode('utf-8'))
    if not password_correct:
        raise HTTPException(status_code = 400, detail = "Password is incorrect.")
    
    return {
        "message" : "User logged in successfully.",
        "user" : user_exists,
        "token" : signJWT(asdict(user_exists))
    }

def get_books(db : Session, skip : int = 0, limit : int = 100):
    return db.query(
        BookStore
    ).offset(skip).limit(limit).all()

def create_book_user(db : Session, book : BookStoreSchema, user_id : int, response_model = dict):
    new_book = BookStore(
        **book.dict(),
        user_id = user_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {
        "message" : "New book created successfully",
        "book" : new_book
    }

def get_user_books(db : Session, user_id : int):
    return db.query(
        BookStore
    ).filter(BookStore.user_id == user_id).all()


