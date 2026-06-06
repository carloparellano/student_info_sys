from flask import Blueprint

courses_bp = Blueprint("courses", __name__, url_prefix="/course")

from . import routes, controller, forms