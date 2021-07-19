from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length

class RegisterForm(FlaskForm):
    name = StringField('Your full name',validators=[DataRequired()])
    email = StringField('Your Email address',validators=[DataRequired(), Email()])
    password = PasswordField('Your password',validators=[DataRequired(),Length(min=8,message="Password must not be less than %(min)d characters")])
    submit = SubmitField('Register')


