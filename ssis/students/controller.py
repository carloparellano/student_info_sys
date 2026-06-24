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


# Allowed sort columns mapped to SQL expressions (whitelist to prevent injection)
SORT_COLUMNS = {
    "student_id": "student.student_id",
    "first_name": "student.first_name",
    "last_name":  "student.last_name",
    "course_code": "student.course_code",
    "college_code": "course.college_code",
    "year_level":  "student.year_level",
    "gender":      "student.gender",
}


COLLEGES   = ['CASS', 'CCS', 'CEBA', 'CED', 'CHS', 'COE', 'CSM']
YEAR_LEVELS = ['1', '2', '3', '4']
GENDERS    = ['Male', 'Female']


def get_students(page=1, per_page=10, sort="student_id", order="asc",
                 college=None, year=None, gender=None, course=None):
    sort_col  = SORT_COLUMNS.get(sort, "student.student_id")
    order_dir = "DESC" if order == "desc" else "ASC"
    db  = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page

    filters, params = [], []
    if college and college in COLLEGES:
        filters.append("course.college_code = %s"); params.append(college)
    if year and year in YEAR_LEVELS:
        filters.append("student.year_level = %s"); params.append(year)
    if gender and gender in GENDERS:
        filters.append("student.gender = %s"); params.append(gender)
    if course:
        filters.append("student.course_code = %s"); params.append(course)

    where = ("WHERE " + " AND ".join(filters)) if filters else ""

    cur.execute(f"""
        SELECT student.student_id, student.first_name, student.last_name,
               student.course_code, student.year_level, student.gender,
               course.college_code, student.student_url
        FROM student
        LEFT JOIN course  ON student.course_code  = course.course_code
        LEFT JOIN college ON course.college_code  = college.college_code
        {where}
        ORDER BY {sort_col} {order_dir}
        LIMIT %s OFFSET %s;
    """, params + [per_page, offset])
    students = cur.fetchall()
    cur.close(); db.close()
    return students


def get_students_count(college=None, year=None, gender=None, course=None):
    db  = get_db()
    cur = db.cursor()

    filters, params = [], []
    if college and college in COLLEGES:
        filters.append("course.college_code = %s"); params.append(college)
    if year and year in YEAR_LEVELS:
        filters.append("student.year_level = %s"); params.append(year)
    if gender and gender in GENDERS:
        filters.append("student.gender = %s"); params.append(gender)
    if course:
        filters.append("student.course_code = %s"); params.append(course)

    if filters:
        where = "WHERE " + " AND ".join(filters)
        cur.execute(f"""
            SELECT COUNT(*) FROM student
            LEFT JOIN course ON student.course_code = course.course_code
            {where}
        """, params)
    else:
        cur.execute("SELECT COUNT(*) FROM student")

    count = cur.fetchone()[0]
    cur.close(); db.close()
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


def search_students(query, page=1, per_page=10, sort="student_id", order="asc"):
    sort_col  = SORT_COLUMNS.get(sort, "student.student_id")
    order_dir = "DESC" if order == "desc" else "ASC"
    db  = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    like = f"%{query}%"
    cur.execute(f"""
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
        LEFT JOIN course  ON student.course_code = course.course_code
        LEFT JOIN college ON course.college_code = college.college_code
        WHERE
            student.student_id  LIKE %s
            OR student.first_name   LIKE %s
            OR student.last_name    LIKE %s
            OR student.course_code  LIKE %s
            OR student.year_level   LIKE %s
            OR LOWER(student.gender) = LOWER(%s)
        ORDER BY {sort_col} {order_dir}
        LIMIT %s OFFSET %s;
    """, (like, like, like, like, like, query, per_page, offset))
    students = cur.fetchall()
    cur.close(); db.close()
    return students


def search_students_count(query):
    db  = get_db()
    cur = db.cursor()
    like = f"%{query}%"
    cur.execute("""
        SELECT COUNT(*) FROM student
        WHERE
            student_id  LIKE %s
            OR first_name   LIKE %s
            OR last_name    LIKE %s
            OR course_code  LIKE %s
            OR year_level   LIKE %s
            OR LOWER(gender) = LOWER(%s)
    """, (like, like, like, like, like, query))
    count = cur.fetchone()[0]
    cur.close(); db.close()
    return count


# =========================
# Student File Upload Logic
# =========================

def upload_student_file(file):
    """
    Upload a student image to Cloudinary.
    Returns dict: {'is_success': bool, 'url': str, 'error': str}
    """
    if not file or file.filename == '':
        return {'is_success': False, 'error': 'No file selected'}

    # Validate extension
    allowed = {'png', 'jpg', 'jpeg'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed:
        return {'is_success': False, 'error': 'Only PNG, JPG, and JPEG files are allowed'}

    # Check file size (1MB limit)
    data = file.read()
    if len(data) > 1_000_000:
        return {'is_success': False, 'error': 'File too large (max 1MB)'}

    file.seek(0)
    try:
        result = cloudinary_upload(file, resource_type='image')
        return {'is_success': True, 'url': result['secure_url']}
    except Exception as e:
        return {'is_success': False, 'error': str(e)}
