from flask import Blueprint, request, jsonify, redirect, flash
from flask import render_template
from ssis import mysql

college_bp = Blueprint('college', __name__)

# Add College
@college_bp.route('/', methods=["GET", "POST"])
def college_dashboard():
    if request.method == "POST":
        college_code = request.form.get("college_code")
        college_name = request.form.get("college_name")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM college WHERE college_code = %s", (college_code,))
        existing_college = cur.fetchone()

        if existing_college:
            flash("College is Already Existed", "danger")
        else:
            cur.execute("INSERT INTO college (college_code, college_name) VALUES (%s, %s)", (college_code, college_name))
            mysql.connection.commit()

    cur = mysql.new_cursor(dictionary=True)
    cur.execute("SELECT * FROM college")
    colleges = cur.fetchall()
    return render_template("college.html", colleges=colleges)


# Update College
@college_bp.route('/update/<college_code>', methods=["POST"])
def update_college(college_code):
    _college_code = request.form.get("college_code")
    college_name = request.form.get("college_name")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE college SET college_code = %s, college_name = %s WHERE college_code = %s", (_college_code, college_name, college_code,))
    mysql.connection.commit()
    return redirect('/college/')

# Delete College
@college_bp.route('/delete/<college_code>', methods=["DELETE"])
def delete_college(college_code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM college WHERE college_code = %s", (college_code,))
    mysql.connection.commit()
    return jsonify({ "success": True })

# Search College
@college_bp.route('/search/', methods=['GET'])
def college_search():
    query = request.args.get("query")
    if query:
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE college_code LIKE %s OR college_name LIKE %s", (f"%{query}%", f"%{query}%"))
        colleges = cur.fetchall()
        return render_template("college.html", colleges=colleges, query=query)
    else:
        # If no search query is provided, handle this case according to your application logic
        return redirect('/college/')
