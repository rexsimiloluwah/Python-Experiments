from .db import db  
from marshmallow import fields, Schema, validate, ValidationError
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

class Project(db.Document):
    name = db.StringField(
        required = True,
        unique = False,
        max_length = 350
    )

    description = db.StringField(
        required = False,
        max_length = 500
    )

    department = db.StringField(
        required = True
    )

    tags = db.ListField(
        db.StringField(), required = True
    )
    
    timestamp = db.DateTimeField(
        default = datetime.datetime.utcnow
    )

    user = db.ReferenceField('User')

class User(db.Document):
    firstname = db.StringField(
        required = True,
        unique = False,
        max_length = 50
    )

    lastname = db.StringField(
        required = True,
        unique = False,
        max_length = 50
    )

    email = db.EmailField(
        required = True,
        unique = True
    )

    country = db.StringField(
        required = True
    )

    university = db.StringField(
        required = True
    )

    password = db.StringField(
        required = True
    )

    projects = db.ListField(
        db.ReferenceField('Project', reverse_delete_rule = db.PULL)
    )

    created_at = db.DateTimeField(
        default = datetime.datetime.utcnow
    )

    def to_json(self):
        return {
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "email" : self.lastname,
            "country" : self.country,
            "university" : self.university
        }

    # This hashes the password for secure data storage
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    # This compares a password and a hashed password for correctness
    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Project, 'user', db.CASCADE)

    
class UserRegisterSchema(Schema):
    id = fields.String(
        dump_only = True
    )

    firstname = fields.String(
        required = True,
        validate = validate.Length(min = 2)
    )

    lastname = fields.String(
        required = True,
        validate = validate.Length(min = 2)
    )

    email = fields.Email(
        required = True
    )

    country = fields.String(
        required = True
    )

    university = fields.String(
        required = True
    )

    password = fields.String(
        required = True
    )

    projects = fields.List(
        fields.Dict(),
        required = False
    )

    created_at = fields.DateTime(
    )


class UserLoginSchema(Schema):

    email = fields.Email(
        required = True
    )

    password = fields.String(
        required = True
    )

class ProjectSchema(Schema):

    id = fields.String(
        required = True, 
        dump_only = True
    )

    name = fields.String(
        required = True
    )

    description = fields.String(
        required = False
    )

    department = fields.String(
        required = True
    )

    tags = fields.List(
        fields.String(), required = True
    )

    user = fields.String(
        required = True,
        dump_only = True
    )

    timestamp = fields.DateTime(

    )

