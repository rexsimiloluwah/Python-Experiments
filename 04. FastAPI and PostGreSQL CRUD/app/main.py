import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware 
from db.models import Base, BookStore
from schemas import BookStoreSchema
from config import engine, Session
from routers import user, bookstore
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from dependency import get_db

Base.metadata.create_all(bind = engine)

BASE_URL = '/api/books'

app = FastAPI()

app.include_router(user.router, tags = ["Users"], prefix = "/api/user")
app.include_router(bookstore.router, tags = ["Bookstore"], prefix = "/api/bookstore")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "message": "An error occurred",
            "loc" : exc.errors()[0]["loc"],
            "detail": exc.errors()[0]["msg"]
        }),
    )

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)

