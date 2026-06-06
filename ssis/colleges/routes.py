from flask import render_template, request, redirect, flash, jsonify
from .forms import CollegeForm
from .controller import (
    get_colleges,
    create_college,
    update_college_db,
    delete_college_db,
    search_colleges
)
from . import college_bp

@college_bp.route("/", methods=["GET", "POST"])
def college_dashboard():
    form = CollegeForm()

    if form.validate_on_submit():
        if not create_college(form):
            flash("College is Already Existed", "danger")
        else:
            flash("College added successfully!", "success")
            return redirect("/college/")

    colleges = get_colleges()
    return render_template("college.html", colleges=colleges, form=form)


@college_bp.route("/update/<college_code>", methods=["POST"])
def update_college(college_code):
    update_college_db(college_code, request.form)
    return redirect("/college/")


@college_bp.route("/delete/<college_code>", methods=["POST"])
def delete_college(college_code):
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            delete_college_db(college_code)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e)), 400
    # Fallback for non-AJAX
    delete_college_db(college_code)
    return redirect("/college/")


@college_bp.route("/search/", methods=["GET"])
def college_search():
    query = request.args.get("query")
    if not query:
        return redirect("/college/")

    colleges = search_colleges(query)
    return render_template("college.html", colleges=colleges, query=query)
