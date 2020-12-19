#### Working with FastAPI in Python - The Basics 

To run the todoapi :- 

##### Create and activate a virtual environment :- 
```
$ python -m venv env
$ source env/Scripts/activate (For windows)
$ source env/bin/activate (For Ubuntu)
```

##### Install the requirements.txt file
```
$ pip install -r requirements.txt
```

##### Run the app using uvicorn
```
$ cd todoapi
$ uvicorn main:app
```

##### Testing the app
- Navigate to http://127.0.0.1/8000 
- View Swagger UI/OpenAPI auto-generated docs at http://127.0.0.1/8000/docs