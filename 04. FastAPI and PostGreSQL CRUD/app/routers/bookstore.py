from fastapi import Depends, HTTPException, APIRouter, Header
from fastapi.exceptions import ValidationError 
from config import engine, Session 
from typing import Optional, List
from db.models import BookStore, User 
from schemas import UserSchema, UserCreateSchema, BookStoreSchema 
from utils import get_books, create_book_user, decodeJWT, get_user_books
from dependency import get_db

router = APIRouter()

@router.get("/", response_model = List[BookStoreSchema])
def get_bookstore(db : Session = Depends(get_db), skip : int = 0, limit : int = 100):
    try:
        return get_books(db = db, skip = skip, limit = limit)
    except ValidationError as err:
        raise HTTPException(status_code = 404, detail = "No books found in database.")

@router.get("/user", response_model = dict) 
def fetch_books_by_user(db : Session = Depends(get_db), token : Optional[str] = Header(None)):
    if not token:
        raise HTTPException(status_code = 400, detail = "Please enter your auth token.")
    try:
        user =  decodeJWT(token)
    except ValidationError as err:
        raise HTTPException(status_code = 400, detail = err)

    if(user):
        user_id = user["id"]
        books = get_user_books(db = db, user_id = user_id)
        return {
            "message" : f"Successfully fetched {len(books)} books for user.",
            "data" : books
        }

@router.post('/', response_model = dict)
def add_book(book : BookStoreSchema, db : Session = Depends(get_db), token : Optional[str] = Header(None)):
    if not token:
        raise HTTPException(status_code = 400, detail = "Please enter your auth token.")
    try:
        user =  decodeJWT(token)
    except ValidationError as err:
        raise HTTPException(status_code = 400, detail = err)

    if(user):
        user_id = user["id"]
        return create_book_user(db = db, book = book, user_id = user_id)

