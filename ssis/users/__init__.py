from flask import Blueprint

user_bp = Blueprint("users", __name__, url_prefix="/auth")

from . import routes, controller, forms
