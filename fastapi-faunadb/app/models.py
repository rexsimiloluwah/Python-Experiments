"""
    models.py
    ------------------------------------------------------------
    Schemas for the request models, using pydantic data validation.
"""

import re
import pytz
import validators
from datetime import datetime
from enum import Enum
from pydantic import BaseModel,Field,EmailStr,constr,validator
from typing import Dict,Optional,List

class TweetCategoryEnum(Enum):
    sports = 'sports'
    entertainment = 'entertainment'
    random = 'random'
    business = 'business'
    finance = 'finance'
    research = 'research'
    investment = 'investment'
    technology = 'technology'
    science = 'science'
    analytics = 'analytics'
    legal = 'legal'
    news = 'news'
    politics = 'politics'
    games = 'games'
    banter = 'banter'

class UserBase(BaseModel):
    fullname: str 
    email: EmailStr 
    username: str
    website: str = None
    status: Optional[constr(max_length = 500)]
    active: bool = True
    blocked: bool = False
    date_of_birth: datetime = None 
    profile_image_url: str = None 

class UserRegister(UserBase):
    password: str 
    created_at: datetime = datetime.now(pytz.UTC)
    updated_at: datetime = datetime.now(pytz.UTC)

    @validator('password')
    def validate_password(cls,v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,50}$"
        if len(v) < 8:
            raise ValueError("Pasword must be longer than 8 characters.")
        password_valid = re.search(re.compile(pattern), v)
        if not password_valid:
            raise ValueError("Password must contain an uppercase letter, lowercase letter, digit, and special character.")
        return v.strip()

class UserOutput(UserBase):
    followers_count: int = 0
    following_count: int = 0

class UserSignIn(BaseModel):
    email: EmailStr 
    password: str 

class UpdateUserProfile(BaseModel):
    fullname: str = None
    username: str = None
    website: str = None
    status: Optional[constr(max_length = 500)]
    active: bool = True
    date_of_birth: datetime = None 
    profile_image_url: str = None 

class Tweet(BaseModel):
    tweet: str 
    category: TweetCategoryEnum = None 
    tags: List[str] = None
    created_at: datetime = datetime.now(pytz.UTC)
    updated_at: datetime = datetime.now(pytz.UTC)

    @validator('tweet')
    def validate_tweet(cls,v):
        if len(tweet) > 600:
            raise ValueError("Tweet must not be longer than 600 characters.")
        return v.strip()

class Comment(BaseModel):
    comment: str 

    @validator('comment')
    def validate(cls,v):
        if len(comment) > 500:
            raise ValueError("Comment must not be longer than 500 characters.")
        return v.strip()

class RefreshTokenOutput(BaseModel):
    access_token: str
    refresh_token: str 
    expires_at: datetime 
    refreshed_at: datetime 

