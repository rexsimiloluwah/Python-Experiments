from flask import Flask,make_response,abort 
from flask_bootstrap import Bootstrap 
from users import users_blueprint
from products import products_blueprint 
from model import db

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object("config.DevelopmentConfig")

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(users_blueprint, url_prefix="/")
# app.register_blueprint(products_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
