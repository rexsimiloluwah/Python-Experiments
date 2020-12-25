from typing import List, Optional
from pydantic import BaseModel, constr, EmailStr
from datetime import datetime
from enum import Enum

# Enum for the Category Enum
class CategoryEnum(str, Enum):
    action = 'action'
    comic = 'comic'
    fantasy = 'fantasy'
    adventure = 'adventure'
    literary_fiction = 'literary fiction'
    science_fiction = 'science fiction'
    history = 'history'
    others = 'others'
    academics = 'academics'

# Define pydanctic model
class BookStoreSchema(BaseModel):
    title: Optional[constr(max_length = 300)]
    description: Optional[constr(max_length = 300)]
    category: CategoryEnum
    author: str
    price: int
    quantity: int
    published_year: int = None
    bestseller: bool = False
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True 
        schema_extra = {
            "example" : {
                "title" : "The Subtle Art of not giving a fuck.",
                "description" : "A counter-intuitive approach to living a great life.",
                "category" : "others",
                "author" : "Mark Mason",
                "price" : 300,
                "quantity" : 12,
                "published_year" : 200,
                "bestseller" : True,
                "created_at" : "2020-12-24T13:21:12.500286"
            }
        }

# Define pydanctic schema for User
class UserBaseSchema(BaseModel):
    email: EmailStr
    firstname: Optional[constr(max_length = 200)]
    lastname: Optional[constr(max_length = 200)]

class UserCreateSchema(UserBaseSchema):
    password: Optional[constr(min_length = 8)]

    class Config:
        schema_extra = {
            "example" : {
                "email" : "donaldtrump@gmail.com",
                "firstname" : "Donald",
                "lastname" : "Trump",
                "password" : "njdkccjkbwjkdfb90ibkwed"
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr 
    password: Optional[constr(min_length = 8)]

    class Config:
        schema_extra = {
            "example" : {
                "email" : "youremail@gmail.com",
                "password" : "yourpassword"
            }
        }
    
class UserSchema(UserCreateSchema):
    active : bool = False 
    books : List[BookStoreSchema] = []
    created_at: datetime = datetime.now() 

    class Config:
        orm_mode = True 