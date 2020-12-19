## Building a production-grade API with FlaskRestFul and Mongodb

### What is this repository for ?

This repository documents how to build a CRUD API with JWT Authentication capabilities with FlaskRestful and Mongo.db. I created this because there are few resources online which discuss how to use NoSQL databases in Python and Flask projects. I hope someone finds this helpful !

### Overview of the application 

The application is a simple CRUD API for Project management. The API supports the following functionalities :- 
- User Authentication (Login, Register, and Logout) using Json Web Tokens for security.
- CRUD functionality to help users create, update, and delete projects and also view other projects.

### Structure of the application 

The application consists of the following main components :- 
- Databases :- This contains files for connecting and communicating with the Mongo.db database using the Flask_Mongoengine extension. Flask Mongoengine is an extension for the Mongoengine ODM (Object Document Mapper) used to simplify integration with the Flask app. It also consists of the 'models.py' file which define the schemas and serializers. 

- Resources:- This consists of controllers and routes for the API. 

- Main app 

### Configuration 

Create a new .env file, Copy the contents of .env.sample in there and replace them with your configuration  details.

### Running the Application 

##### Clone the code
```
$ git clone https://github.com/rexsimiloluwah/Python-Experiments.git
$ cd '01. FlaskRestful and MongoDB'
```

##### Create and activate virtual environment 
```
$ python3 -m venv env
$ source activate env/Scripts/activate (For windows)
$ source activate env/bin/activate (For Ubuntu)
```

##### Install requirements 
```
$ pip install -r requirements.txt
```

###### Run application
```
$ python app.py
```

###### Test the running app on http://127.0.0.1:5000

### Documentation
Coming soon !


