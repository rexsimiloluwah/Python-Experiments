from fastapi import APIRouter, HTTPException
from .schemas import HeartDiseaseSchema
from .train import HeartDiseaseModel 
from pydantic import BaseModel, constr, ValidationError
from typing import Optional
from enum import Enum

heartdisease = HeartDiseaseModel()
heartdisease.load_model()

router = APIRouter()

@router.post('/predict', response_model = dict) 
async def predict_features(features : HeartDiseaseSchema):
    print(features.dict())
    try:
        return heartdisease.predict(features.dict())
    except (ValidationError) as err:
        raise HTTPException(status_code = 400, detail = err)
