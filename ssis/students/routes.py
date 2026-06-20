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
    search_students_count,
    SORT_COLUMNS,
    COLLEGES,
    YEAR_LEVELS,
    GENDERS,
)
from . import student_bp
from ssis.utils import login_required


def _get_filters(args):
    """Parse and sanitise all shared filter/sort params from request.args."""
    sort    = args.get("sort", "student_id")
    order   = args.get("order", "asc")
    college = args.get("college", "")
    year    = args.get("year", "")
    gender  = args.get("gender_filter", "")
    course  = args.get("course_filter", "")
    page    = int(args.get("page", 1))

    if sort not in SORT_COLUMNS:
        sort = "student_id"
    if order not in ("asc", "desc"):
        order = "asc"
    if college not in COLLEGES:
        college = ""
    if year not in YEAR_LEVELS:
        year = ""
    if gender not in GENDERS:
        gender = ""

    return sort, order, college, year, gender, course, page


@student_bp.route("/", methods=["GET", "POST"])
@login_required
def student_dashboard():
    all_courses = get_courses()
    form = StudentForm()
    form.course_code.choices = [(c["course_code"], c["course_code"]) for c in all_courses]

    sort, order, college, year, gender, course, page = _get_filters(request.args)
    per_page = 10

    if form.validate_on_submit():
        if not create_student(form):
            flash("The ID Number is Already Existed", "danger")
        else:
            flash("Student added successfully!", "success")
            return redirect("/student/")

    students = get_students(page=page, per_page=per_page,
                            sort=sort, order=order,
                            college=college, year=year,
                            gender=gender, course=course)
    total = get_students_count(college=college, year=year,
                               gender=gender, course=course)
    return render_template(
        "student.html",
        students=students,
        courses=all_courses,
        form=form,
        page=page, per_page=per_page, total=total,
        sort=sort, order=order,
        college=college, year=year,
        gender_filter=gender, course_filter=course,
        colleges=COLLEGES,
    )


@student_bp.route("/upload_student_image", methods=["POST"])
@login_required
def upload_student_image():
    file = request.files.get("upload")
    result = upload_student_file(file)
    return jsonify(result), (200 if result["is_success"] else 413)


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
    if not query:
        return redirect("/student/")

    all_courses = get_courses()
    form = StudentForm()
    form.course_code.choices = [(c["course_code"], c["course_code"]) for c in all_courses]

    sort, order, college, year, gender, course, page = _get_filters(request.args)
    per_page = 10

    students = search_students(query, page=page, per_page=per_page,
                               sort=sort, order=order)
    total = search_students_count(query)
    return render_template(
        "student.html",
        students=students,
        courses=all_courses,
        form=form,
        query=query,
        page=page, per_page=per_page, total=total,
        sort=sort, order=order,
        college=college, year=year,
        gender_filter=gender, course_filter=course,
        colleges=COLLEGES,
    )
