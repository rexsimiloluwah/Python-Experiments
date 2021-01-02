### My First try at building a CRUD app with FastAPI

Building a CRUD (bookstore) API with FastAPI and PostGreSQL with some CRUD capabilities and user authentication.

Tools/Technologies and Libraries used :- 
- Python (FastAPI, Pydantic and SQLAlchemy)
- PostGreSQL 
- PyJWT and Bcrypt
- Uvicorn 
- Python-dotenv 

Setting up :- 

- Clone the repository 

- Switch to app working directory

- Create and activate virtual environment
```
$ python3 -m venv env
$ source env/Scripts/activate (windows) or source env/bin/activate (Ubuntu)
```

- Database configuration
Create a new PostGreSQL database and modify the parameters in the .env, Check .env.sample 

- Running/ Testing the app

```
$ python main.py
```

- View app at http://localhost:8000 
- View interactive docs UI at http://localhost:8000/docs 

![Open API docs UI](openapidocsui.png)





