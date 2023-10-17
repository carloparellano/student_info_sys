from flask import Blueprint
from flask import render_template

course_bp = Blueprint('course', __name__)

@course_bp.route('/')
def course_dashboard():
    return render_template("course.html", courses=[])