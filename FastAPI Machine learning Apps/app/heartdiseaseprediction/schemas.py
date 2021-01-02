from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class GenderEnum(str, Enum):
    female = "female"
    male = "male"

    def __str__(self):
        return str(self.value)

class YesNoEnum(str, Enum):
    yes = "yes"
    no = "no"

    def __str__(self):
        return str(self.value)

class HeartDiseaseSchema(BaseModel):
    sysBP : int
    glucose : int
    age : int 
    totChol : int 
    cigsPerDay : int 
    diaBP : int 
    prevalentHyp : YesNoEnum
    diabetes : YesNoEnum
    BPMeds : YesNoEnum
    gender : GenderEnum
    weight : int 
    height : int 
    prevalentStroke : YesNoEnum

    class Config:
        schema_extra = {
            "example" : {
                "sysBP" : 40,
                "glucose" : 20,
                "age" : 12,
                "totChol" : 130,
                "cigsPerDay" : 1,
                "diaBP" : 10,
                "prevalentHyp" : "yes",
                "diabetes" : "yes",
                "BPMeds" : "no",
                "gender" : "male",
                "weight" : 23,
                "height" : 4,
                "prevalentStroke" : "yes"
                }
        }