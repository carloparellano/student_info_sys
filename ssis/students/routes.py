from flask import render_template, request, redirect, flash, jsonify
from .forms import StudentForm
from .controller import (
    get_courses,
    get_students,
    create_student,
    update_student_db,
    delete_student_db,
    search_students,
    upload_student_file,
    get_students_count,
    search_students_count
)
from . import student_bp
from ssis.utils import login_required


@student_bp.route("/", methods=["GET", "POST"])
@login_required
def student_dashboard():
    form = StudentForm()
    courses = get_courses()
    form.course_code.choices = [(c["course_code"], c["course_code"]) for c in courses]

    page = int(request.args.get("page", 1))
    per_page = 10

    if form.validate_on_submit():
        if not create_student(form):
            flash("The ID Number is Already Existed", "danger")
        else:
            flash("Student added successfully!", "success")
            return redirect("/student/")

    students = get_students(page=page, per_page=per_page)
    total = get_students_count()
    return render_template(
        "student.html",
        students=students,
        courses=courses,
        form=form,
        page=page,
        per_page=per_page,
        total=total
    )


@student_bp.route("/upload_student_image", methods=["POST"])
@login_required
def upload_student_image():
    file = request.files.get("upload")
    result = upload_student_file(file)  # call controller
    status_code = 200 if result["is_success"] else 413
    return jsonify(result), status_code


@student_bp.route("/update/<student_id>", methods=["POST"])
@login_required
def update_student(student_id):
    update_student_db(student_id, request.form)
    return redirect("/student/")


@student_bp.route("/delete/<student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    delete_student_db(student_id)
    return jsonify(success=True)


@student_bp.route("/search/", methods=["GET"])
@login_required
def student_search():
    query = request.args.get("query")
    page = int(request.args.get("page", 1))
    per_page = 10
    if not query:
        return redirect("/student/")

    students = search_students(query, page=page, per_page=per_page)
    total = search_students_count(query)
    return render_template("student.html", students=students, query=query, page=page, per_page=per_page, total=total)
