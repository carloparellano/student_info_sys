from flask import Blueprint
from flask import render_template

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
def student_dashboard():
    return render_template("student.html", students=[])