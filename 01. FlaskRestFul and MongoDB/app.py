from flask import Flask, Response, jsonify, request
from flask_restful import Resource, Api
from databases.db import init_db
from resources.routes import init_routes
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    api = Api(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    app.config.from_object('config.DevelopmentConfig')
    init_db(app)
    init_routes(api)
    return app 

app = create_app()


if __name__ == "__main__":
    app.run(threaded = True)