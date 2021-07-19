from utils import check_valid_id
from typing import List, Dict
from helpers import User, Tweet
from fastapi.routing import APIRouter
from fastapi import status, Request, Response, Header, HTTPException
from models import UserBase, UserRegister, UserSignIn, UpdateUserProfile

router = APIRouter()

@router.get('/tweets', response_model=Dict)
def get_all_tweets():
    """Get all tweets"""
    tweets = Tweet().get_all_tweets()
    if not tweets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No Tweets found.'
        )
    return {
        'status':True,
        'message':f'Successfully fetched {len(tweets)} tweets.',
        'data':tweets
    }

@router.get('/tweets/{id}', response_model=Dict)
def get_tweet_by_id(id:str):
    """Get tweet by id"""
    if not check_valid_id(id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Tweet ID is invalid.'
        )
    
    tweet = Tweet().get_tweet(id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This tweet does not exist.'
        )
    return {
        'status':True,
        'message':f'Tweet successfully fetched.',
        'data':tweet['data']
    }