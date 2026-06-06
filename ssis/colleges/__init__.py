from flask import Blueprint

college_bp = Blueprint("college", __name__, url_prefix="/college")

from . import routes, controller, forms