from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

#Instantiate SQLAlchemy and Marshmallow 
db = SQLAlchemy()
ma = Marshmallow()

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fullname = db.Column(
        db.String(80),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(80),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

class UserSchema(ma.Schema):
    id = fields.Integer(
    )

    fullname = fields.String(
        required=True
    )

    email = fields.String(
        required=True
    )

    password = fields.String(
        required=True
    )

    created_at = fields.Date(
        required=False,
        default=datetime.now()
    )