from flask import Blueprint, request, render_template, jsonify, redirect, flash
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
        cur.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        existing_student = cur.fetchone()
        
        if existing_student:
            flash("The ID Number is Already Existed", "danger")
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (student_id, first_name, last_name, course_code, year_level, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                        (student_id, first_name, last_name, course_code, year_level, gender))
            mysql.connection.commit()

    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()
    
    course_cur = mysql.new_cursor(dictionary=True)
    course_cur.execute("SELECT * FROM course")
    courses = course_cur.fetchall()
    return render_template("student.html", students=students, courses=courses)


@student_bp.route('/update/<student_id>', methods=["POST"])
def update_student(student_id):
    new_student_id = request.form.get("student_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    course_code = request.form.get("course_code")
    year_level = request.form.get("year_level")
    gender = request.form.get("gender")
    cur = mysql.connection.cursor()
    print(f"UPDATE student SET student_id = {new_student_id}, first_name = {first_name}, last_name = {last_name}, course_code = {course_code}, year_level = {year_level}, gender = {gender} WHERE student = {student_id}")
    cur.execute("UPDATE student SET student_id = %s, first_name = %s, last_name = %s, course_code = %s, year_level = %s, gender = %s WHERE student_id = %s",
                (new_student_id, first_name, last_name, course_code, year_level, gender,student_id,))
    mysql.connection.commit()
    return redirect('/student/')

@student_bp.route('/delete/<student_id>', methods=["DELETE"])
def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
    mysql.connection.commit()
    return jsonify({"success": True})

# Search Course
@student_bp.route('/search/', methods=['GET'])
def student_search():
    query = request.args.get("query")
    if query:
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR course_code LIKE %s OR year_level LIKE %s OR gender LIKE %s", 
                    (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        students = cur.fetchall()
        return render_template("student.html", students=students, query=query)
    else:
        # If no search query is provided, handle this case according to your application logic
        return redirect('/student/')