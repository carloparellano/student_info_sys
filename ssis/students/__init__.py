from flask import Blueprint

student_bp = Blueprint("students", __name__, url_prefix="/student")

from . import routes, controller, forms