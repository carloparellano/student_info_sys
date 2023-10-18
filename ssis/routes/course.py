from flask import Blueprint, request, render_template
from ssis import mysql

course_bp = Blueprint('course', __name__)

@course_bp.route('/', methods=["GET", "POST"])
def course_dashboard():
    if request.method == "POST":
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        college_code = request.form.get("college_code")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO course (course_code, course_name, college_code) VALUES (%s, %s, %s)", 
                    (course_code, course_name, college_code))
        mysql.connection.commit()

    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    
    return render_template("course.html", courses=courses)
