from flask import Blueprint, request, render_template
from ssis import mysql

student_bp = Blueprint('student', __name__)

@student_bp.route('/', methods=["GET", "POST"])
def student_dashboard():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        course_code = request.form.get("course_code")
        year_level = request.form.get("year_level")
        gender = request.form.get("gender")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (student_id, first_name, last_name, course_code, year_level, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                    (student_id, first_name, last_name, course_code, year_level, gender))
        mysql.connection.commit()

    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()

    return render_template("student.html", students=students)
