import mysql.connector
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST


def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
