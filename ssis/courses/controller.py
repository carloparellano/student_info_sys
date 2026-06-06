from ssis.db_connection import get_db
from .forms import CourseForm


def get_colleges():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM college")
    colleges = cur.fetchall()
    cur.close()
    db.close()
    return colleges


def get_courses(page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute("SELECT * FROM course LIMIT %s OFFSET %s", (per_page, offset))
    courses = cur.fetchall()
    cur.close()
    db.close()
    return courses


def get_courses_count():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM course")
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count


def create_course(form):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT 1 FROM course WHERE course_code = %s",
        (form.course_code.data,)
    )

    if cur.fetchone():
        cur.close()
        db.close()
        return False

    cur.execute(
        """
        INSERT INTO course (course_code, course_name, college_code)
        VALUES (%s, %s, %s)
        """,
        (
            form.course_code.data,
            form.course_name.data,
            form.college_code.data,
        )
    )

    db.commit()
    cur.close()
    db.close()
    return True


def update_course_db(course_code, data):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        UPDATE course
        SET course_code=%s, course_name=%s, college_code=%s
        WHERE course_code=%s
        """,
        (
            data["course_code"],
            data["course_name"],
            data["college_code"],
            course_code,
        )
    )
    db.commit()
    cur.close()
    db.close()


def delete_course_db(course_code):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM course WHERE course_code = %s", (course_code,))
    db.commit()
    cur.close()
    db.close()


def search_courses(query, page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute(
        """
        SELECT * FROM course
        WHERE course_code LIKE %s
           OR course_name LIKE %s
           OR college_code LIKE %s
        LIMIT %s OFFSET %s
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%", per_page, offset),
    )
    courses = cur.fetchall()
    cur.close()
    db.close()
    return courses


def search_courses_count(query):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT COUNT(*) FROM course
        WHERE course_code LIKE %s
           OR course_name LIKE %s
           OR college_code LIKE %s
        """,
        (f"%{query}%", f"%{query}%", f"%{query}%"),
    )
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count
