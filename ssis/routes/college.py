from flask import Blueprint, request
from flask import render_template
from ssis import mysql

college_bp = Blueprint('college', __name__)

@college_bp.route('/', methods=["GET", "POST"])
def college_dashboard():
    if request.method == "POST":
        college_code = request.form.get("college_code")
        college_name = request.form.get("college_name")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO college (college_code, college_name) VALUES (%s, %s)", (college_code, college_name))
        mysql.connection.commit()
    
    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM college")
    colleges = cur.fetchall()
         
    return render_template("college.html", colleges=colleges)