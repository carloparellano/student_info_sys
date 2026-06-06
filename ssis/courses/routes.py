from flask import render_template, request, redirect, jsonify, flash
from .forms import CourseForm
from .controller import (
    get_colleges,
    get_courses,
    create_course,
    update_course_db,
    delete_course_db,
    search_courses,
    get_courses_count,
    search_courses_count,
)
from . import courses_bp

@courses_bp.route("/", methods=["GET", "POST"])
def course_dashboard():
    form = CourseForm()

    colleges = get_colleges()
    form.college_code.choices = [
        (c["college_code"], c["college_code"]) for c in colleges
    ]

    page = int(request.args.get("page", 1))
    per_page = 10

    if form.validate_on_submit():
        if not create_course(form):
            flash("Course already exists.", "danger")
        else:
            flash("Course added successfully!", "success")
            return redirect("/course/")

    courses = get_courses(page=page, per_page=per_page)
    total = get_courses_count()
    return render_template(
        "course.html",
        courses=courses,
        colleges=colleges,
        form=form,
        page=page,
        per_page=per_page,
        total=total
    )


@courses_bp.route("/update/<course_code>", methods=["POST"])
def update_course(course_code):
    update_course_db(course_code, request.form)
    return redirect("/course/")


@courses_bp.route("/delete/<course_code>", methods=["POST"])
def delete_course(course_code):
    delete_course_db(course_code)
    return jsonify(success=True)


@courses_bp.route("/courses/delete/<course_code>", methods=["POST"])
def delete_course_ajax(course_code):
    delete_course_db(course_code)
    return jsonify(success=True)


@courses_bp.route("/search/", methods=["GET"])
def course_search():
    query = request.args.get("query")
    page = int(request.args.get("page", 1))
    per_page = 10
    if not query:
        return redirect("/course/")

    courses = search_courses(query, page=page, per_page=per_page)
    total = search_courses_count(query)
    colleges = get_colleges()
    return render_template("course.html", courses=courses, colleges=colleges, query=query, page=page, per_page=per_page, total=total)
