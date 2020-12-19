from flask import Flask, Response, jsonify, request, make_response
from marshmallow import ValidationError
from flask_restful import Resource 
from databases.models import User, UserRegisterSchema, UserLoginSchema
from flask_jwt_extended import create_access_token
import datetime

user_schema_single = UserRegisterSchema()
user_schema_multiple = UserRegisterSchema(many = True)

user_login_schema = UserLoginSchema()

class Auth(Resource):

    def get(self):
        users = User.objects()
        # serialized_response = user_schema_multiple.dump(users)
        print(users)
        
        return make_response(
            {"users" : users},
            200
        )
        


class Register(Resource):

    def post(self):
        body = request.get_json()
        try:
            data = user_schema_single.load(body)
            if User.objects.filter(email = body.get('email')[0]):
                return make_response(
                    {"message" : "User already exists !"},
                    400)
            new_user = User(**data)
            new_user.hash_password()
            new_user.save()
            return {
                "message" : "User Registered successfully !"
            }, 201
            
        except ValidationError as err:
            print(err.messages)
            return make_response(err.messages , 400)


class Login(Resource):

    def post(self):
        body = request.get_json()
        try:
            data = user_login_schema.load(body)
            user = User.objects.filter(email = body.get('email'))[0]
            if user:
                authorized = user.check_password(body.get('password'))
                if not authorized:
                    return make_response(
                        {"message" : "Password is incorrect, Please enter your correct password !"}
                    )

                expires = datetime.timedelta(days = 3)  # Token Expires in 3 days
                access_token = create_access_token(identity = str(user.id), expires_delta = expires)
                user = user_schema_single.dump(user)
                return make_response(
                    {"message" : "Logged in successfully", "user" : user, "token" : access_token}
                )
            else:
                return make_response(
                    {"message" : "User does not exist, Please register to create an account."}
                )
                
        except ValidationError as err:
            print(err.messages)
            return make_response(err.messages, 400)