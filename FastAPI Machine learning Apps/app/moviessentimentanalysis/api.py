from fastapi import APIRouter, HTTPException
from .train import MoviesSentimentModel
from pydantic import BaseModel, constr, ValidationError
from typing import Optional

class TextSchema(BaseModel):
    text : str = None 
    class Config:
        schema_extra = {
            "example" : {
                "text" : "This movie is disgusting"
            }
        }

moviesentimentmodel = MoviesSentimentModel()
moviesentimentmodel._load_model()

router = APIRouter()

@router.post('/predict', response_model = dict) 
async def predict(text : TextSchema):
    try:
        return moviesentimentmodel.predict(text.dict()["text"].lower())
    except (ValidationError) as err:
        raise HTTPException(status_code = 400, detail = err)
