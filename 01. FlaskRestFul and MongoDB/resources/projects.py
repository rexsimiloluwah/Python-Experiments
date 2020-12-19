from flask import Flask, Response, jsonify, request, make_response
from marshmallow import ValidationError
from flask_restful import Resource 
from databases.models import User, Project, UserRegisterSchema, UserLoginSchema, ProjectSchema
from flask_jwt_extended import jwt_required, get_jwt_identity #jwt_required is a decorator used to require auth permissions on certain routes

project_schema_single = ProjectSchema()
project_schema_multiple = ProjectSchema(many = True)

class Projects(Resource):

    def get(self):
        projects = Project.objects()
        print(projects)
        return make_response(
            {"projects" : projects},
            200
        )

    @jwt_required
    def post(self):
        jwt_id = get_jwt_identity()
        body = request.get_json()

        try:
            data = project_schema_single.load(body)
            user = User.objects.get(id = jwt_id)
            project = Project(**body, user = user)
            project.save()
            user.update(push__projects = project)
            user.save()
            return make_response(
                {"message" : "Project added successfully !", "project" : project},
                201
            )

        except ValidationError as err:
            print(err.messages)
            return make_response(err.messages, 400)


class ProjectsDetail(Resource):

    @jwt_required
    def put(self, id):
        jwt_id = get_jwt_identity()
        body = request.get_json()

        try:
            body = request.get_json()
            user = User.objects.get(id = jwt_id)
            project = Project.objects.get(id = id, user = user)
            Project.objects.get(id = id).update(**body)
            return make_response(
                {"message" : "Update successful"},
                200
            )
        except Exception as e:
            return make_response(
                {"message" : e},
                500
                )
    
    @jwt_required
    def delete(self, id):
        jwt_id = get_jwt_identity()
        user = User.objects.get(id = jwt_id)
        project = Project.objects.get(id = id, user = user)
        project.delete()
        return make_response(
            {"message" : "Deleted successfully !"},
            200
        )



    
