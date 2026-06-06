from ssis.db_connection import get_db
from cloudinary.uploader import upload as cloudinary_upload



def get_courses():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    cur.close()
    db.close()
    return courses


def get_students(page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute("""
        SELECT 
            student.student_id,
            student.first_name,
            student.last_name,
            student.course_code,
            student.year_level,
            student.gender,
            course.college_code,
            student.student_url
        FROM student
        JOIN course ON student.course_code = course.course_code
        JOIN college ON course.college_code = college.college_code
        LIMIT %s OFFSET %s;
    """, (per_page, offset))
    students = cur.fetchall()
    cur.close()
    db.close()
    return students


def get_students_count():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM student")
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count


def create_student(form):
    db = get_db()
    cur = db.cursor(dictionary=True)

    # Check if student exists
    cur.execute("SELECT 1 FROM student WHERE student_id = %s", (form.student_id.data,))
    if cur.fetchone():
        cur.close()
        db.close()
        return False

    # Insert student
    cur.execute("""
        INSERT INTO student
        (student_id, first_name, last_name, course_code, year_level, gender, student_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        form.student_id.data,
        form.first_name.data,
        form.last_name.data,
        form.course_code.data,
        form.year_level.data,
        form.gender.data,
        form.student_url.data
    ))

    db.commit()
    cur.close()
    db.close()
    return True


def update_student_db(student_id, data):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE student SET
            student_id=%s,
            first_name=%s,
            last_name=%s,
            course_code=%s,
            year_level=%s,
            gender=%s,
            student_url=%s
        WHERE student_id=%s
    """, (
        data["student_id"],
        data["first_name"],
        data["last_name"],
        data["course_code"],
        data["year_level"],
        data["gender"],
        data["student_url"],
        student_id
    ))
    db.commit()
    cur.close()
    db.close()


def delete_student_db(student_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM student WHERE student_id=%s", (student_id,))
    db.commit()
    cur.close()
    db.close()


def search_students(query, page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute("""
        SELECT 
            student.student_id,
            student.first_name,
            student.last_name,
            student.course_code,
            student.year_level,
            student.gender,
            course.college_code,
            student.student_url
        FROM student
        JOIN course ON student.course_code = course.course_code
        JOIN college ON course.college_code = college.college_code
        WHERE 
            student.student_id LIKE %s
            OR student.first_name LIKE %s
            OR student.last_name LIKE %s
            OR student.course_code LIKE %s
            OR student.year_level LIKE %s
            OR student.gender LIKE %s
        LIMIT %s OFFSET %s;
    """, tuple([f"%{query}%"] * 6) + (per_page, offset))
    students = cur.fetchall()
    cur.close()
    db.close()
    return students


def search_students_count(query):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM student
        WHERE 
            student_id LIKE %s
            OR first_name LIKE %s
            OR last_name LIKE %s
            OR course_code LIKE %s
            OR year_level LIKE %s
            OR gender LIKE %s
    """, tuple([f"%{query}%"] * 6))
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count


# =========================
# Student File Upload Logic
# =========================

def upload_student_file(file):
    """
    Upload a student image to Cloudinary.
    Returns dict: {'is_success': bool, 'url': str, 'error': str}
    """
    if not file:
        return {'is_success': False, 'error': 'Missing file'}

    if len(file.read()) > 1_000_000:  # 1MB limit
        return {'is_success': False, 'error': 'File too large'}

    file.seek(0)
    try:
        result = cloudinary_upload(file)
        return {'is_success': True, 'url': result['secure_url']}
    except Exception as e:
        return {'is_success': False, 'error': str(e)}
