import hashlib
from ssis.db_connection import get_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_user_by_email(email):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    db.close()
    return user


def create_user(email, password):
    if get_user_by_email(email):
        return False  # user already exists

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO user (email, password) VALUES (%s, %s)",
        (email, hash_password(password))
    )
    db.commit()
    cur.close()
    db.close()
    return True


def verify_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return False
    return user["password"] == hash_password(password)
