from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr 
from typing import Optional, List
from datetime import datetime 

# Initialize the app
app = FastAPI(title = "Todo API") 

class Todo(BaseModel):
    name : str
    description : Optional[constr(max_length = 100)]
    priority : str 
    created_at : datetime

todo_store = []

@app.get("/")
def index():
    return {
        "message" : "Welcome to the TODO API, Please go to /docs to interact with the API."
    }

# Working with CRUD - Create, Read, Update, Delete (WITHOUT DATABASES)

# Create
@app.post("/todo/")
async def create_todo(todo : Todo):
    todo_store.append(todo)
    return todo

# Read - List
@app.get("/todo/", response_model = List[Todo])
async def get_all_todos():
    return todo_store 

# Read - Detail
@app.get("/todo/{id}")
async def get_todo_by_id(id : int):
    try:
        return todo_store[id]
    except Exception as e:
        raise HTTPException(status_code=404, detail = e)

# Update 
@app.put("/todo/{id}")
async def update_todo(id : int, todo : Todo):
    try:
        todo_store[id] = todo 
        return todo
    except Exception as e:
        raise HTTPException(status_code=400, detail = e)

# Delete 
@app.delete("/todo/{id}")
async def delete_todo(id : int):
    try:
        obj = todo_store[id]
        todo_store.pop(id)
        return obj 
    except Exception as e:
        raise HTTPException(status_code = 404, detail = "Not deleted.")

