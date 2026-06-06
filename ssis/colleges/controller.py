from ssis.db_connection import get_db  # safe import, no circular dependency


def get_colleges(page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute("SELECT * FROM college LIMIT %s OFFSET %s", (per_page, offset))
    colleges = cur.fetchall()
    cur.close()
    db.close()
    return colleges


def get_colleges_count():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM college")
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count


def create_college(form):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT 1 FROM college WHERE college_code = %s", (form.college_code.data,))
    
    if cur.fetchone():
        cur.close()
        db.close()
        return False

    cur.execute(
        "INSERT INTO college (college_code, college_name) VALUES (%s, %s)",
        (form.college_code.data, form.college_name.data)
    )
    db.commit()
    cur.close()
    db.close()
    return True


def update_college_db(college_code, data):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE college
        SET college_code=%s, college_name=%s
        WHERE college_code=%s
    """, (
        data["college_code"],
        data["college_name"],
        college_code
    ))
    db.commit()
    cur.close()
    db.close()


def delete_college_db(college_code):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM college WHERE college_code=%s", (college_code,))
    db.commit()
    cur.close()
    db.close()


def search_colleges(query, page=1, per_page=10):
    db = get_db()
    cur = db.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cur.execute("""
        SELECT * FROM college
        WHERE college_code LIKE %s
           OR college_name LIKE %s
        LIMIT %s OFFSET %s
    """, (f"%{query}%", f"%{query}%", per_page, offset))
    colleges = cur.fetchall()
    cur.close()
    db.close()
    return colleges


def search_colleges_count(query):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM college
        WHERE college_code LIKE %s
           OR college_name LIKE %s
    """, (f"%{query}%", f"%{query}%"))
    count = cur.fetchone()[0]
    cur.close()
    db.close()
    return count
