from flask import Blueprint, request, render_template, jsonify, redirect, flash
from ssis import mysql

course_bp = Blueprint('course', __name__)

@course_bp.route('/', methods=["GET", "POST"])
def course_dashboard():
    if request.method == "POST":
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        college_code = request.form.get("college_code")
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course WHERE course_code = %s", (course_code,))
        existing_course = cur.fetchone()

        if existing_course:
            flash("Course is Already Existed.", "danger")
        else:
            cur.execute("INSERT INTO course (course_code, course_name, college_code) VALUES (%s, %s, %s)", 
                        (course_code, course_name, college_code))
            mysql.connection.commit()
            
    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()

    college_cur = mysql.new_cursor(dictionary=True)
    college_cur.execute("SELECT * FROM college")
    colleges = college_cur.fetchall()
    return render_template("course.html", courses=courses, colleges=colleges)
   
@course_bp.route('/update/<course_code>', methods=["POST"])
def update_course(course_code):
    new_course_code = request.form.get("course_code")
    course_name = request.form.get("course_name")
    college_code = request.form.get("college_code")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE course SET course_code = %s, course_name = %s, college_code = %s WHERE course_code = %s", 
                (new_course_code, course_name, college_code,course_code,))
    mysql.connection.commit()
    return redirect('/course/')

@course_bp.route('/delete/<course_code>', methods=["DELETE"])
def delete_course(course_code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM course WHERE course_code = %s", (course_code,))
    mysql.connection.commit()
    return jsonify({"success": True})

# Search Course
@course_bp.route('/search/', methods=['GET'])
def course_search():
    query = request.args.get("query")
    if query:
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE course_code LIKE %s OR course_name LIKE %s OR college_code LIKE %s", (f"%{query}%", f"%{query}%", f"%{query}%"))
        courses = cur.fetchall()
        return render_template("course.html", courses=courses, query=query)
    else:
        # If no search query is provided, handle this case according to your application logic
        return redirect('/course/')