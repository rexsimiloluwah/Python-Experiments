from typing import Optional
from fastapi import FastAPI
from datetime import datetime

# Working with Pydantic
from pydantic import BaseModel, constr

# Initialize the app
app = FastAPI()

# Building Models using Pydantic
class Task(BaseModel): #Inherits from BaseModel
    name : str
    description : Optional[constr(max_length = 100)]
    priority : str
    created_at : datetime = None


@app.get("/")
async def index():
    return {
        "message" : "Hello World !"
    }

# Path and Query parameters
@app.get("/greeting/{name}")  #Path parameters
async def greeting(name : str):
    return {
        "message" : f"Good morning, My name is {name}"
    }

@app.get("/greeting/") #Query parameters
async def query_greeting(name : str, age : Optional[int]):
    return {
        "message" : f"Good morning, My name is {name} and I am {age} years old."
    }

#Working with post requests and pydantic Base Model
@app.post("/")
async def create_task(task : Task):
    return task

# Using post request with Pydantic base model and query/path parameters
@app.post("/{urgent}")
async def create_task(urgent : bool, task : Task):
    return {
        "urgent" : urgent,
        **task.dict()
    }




