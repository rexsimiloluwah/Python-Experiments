from flask import make_response,abort,jsonify,render_template,redirect

from . import forms 
from . import users_blueprint
from model import UserModel,UserSchema,db
import json

user_schema_single = UserSchema()
user_schema_multiple = UserSchema(many=True)

# Home page 
@users_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Registration page
@users_blueprint.route("/register", methods=["GET","POST"])
def register():
    message = ''
    form = forms.RegisterForm()

    if form.is_submitted():
        print(form.validate_on_submit())
        if form.validate_on_submit():
            d = json.dumps({
                "fullname":form.name.data,
                "email":form.email.data,
                "password":form.password.data
            })

            d = user_schema_single.loads(d)

            new_user = UserModel(
                fullname=d["fullname"],
                email=d["email"],
                password=d["password"]
            )

            db.session.add(new_user)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "User could not be saved."
            
            return f"Welcome {form.name.data}."
        else:
            message = "Form is invalid."
    return render_template('register.html',form=form, message=message)

@users_blueprint.route("/users",methods=["GET"])
def get_users():
    d = UserModel.query.all()
    serialized_response = user_schema_multiple.dump(d)
    return make_response({"users":serialized_response},200)

@users_blueprint.route("/users/<int:id>",methods=["GET"])
def get_user_by_id(id):
    d = UserModel.query.filter_by(id=id).first_or_404()
    if d:
        serialized_response = user_schema_single.dump(d)
        return make_response(serialized_response,200)
    else:
        return make_response({"message":"No user found,Please register."},404)

