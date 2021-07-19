from flask import Blueprint 

products_blueprint = Blueprint('products', __name__, template_folder='templates')

from . import routes