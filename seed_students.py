"""
seed_students.py
----------------
Generates 1500 students with unique YYYY-NNNN student IDs.
Run from the project root:
    python seed_students.py

Requires the app's .env to be present (DB credentials).
Skips any student ID that already exists in the DB.
"""

import random
import string
from dotenv import load_dotenv

load_dotenv('.env')

from ssis.db_connection import get_db

# ── Sample name data ──────────────────────────────────────────────
FIRST_NAMES = [
    "James", "Maria", "John", "Patricia", "Robert", "Jennifer", "Michael",
    "Linda", "William", "Barbara", "David", "Susan", "Richard", "Jessica",
    "Joseph", "Sarah", "Thomas", "Karen", "Charles", "Lisa", "Juan", "Ana",
    "Mark", "Donna", "Donald", "Carol", "George", "Ruth", "Kenneth", "Sharon",
    "Steven", "Michelle", "Edward", "Laura", "Brian", "Emily", "Ronald",
    "Kimberly", "Anthony", "Deborah", "Kevin", "Dorothy", "Jason", "Amy",
    "Matthew", "Angela", "Gary", "Ashley", "Timothy", "Melissa", "Jose",
    "Brenda", "Larry", "Pamela", "Jeffrey", "Emma", "Frank", "Nicole",
    "Scott", "Helen", "Eric", "Samantha", "Stephen", "Katherine", "Andrew",
    "Christine", "Raymond", "Debra", "Gregory", "Rachel", "Joshua", "Carolyn",
    "Jerry", "Janet", "Dennis", "Maria", "Walter", "Catherine", "Patrick",
    "Heather", "Peter", "Diane", "Harold", "Julie", "Douglas", "Joyce",
    "Henry", "Victoria", "Carl", "Kelly", "Arthur", "Christina", "Ryan",
    "Joan", "Roger", "Evelyn", "Joe", "Lauren", "Juan", "Judith", "Jack",
    "Olivia", "Albert", "Frances", "Jonathan", "Martha",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Cruz", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson",
    "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
    "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo",
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    "Santos", "Dela Cruz", "Reyes", "Bautista", "Aquino", "Villanueva",
    "Fernandez", "Castro", "Romero", "Navarro",
]


def generate_unique_ids(existing_ids: set, count: int) -> list:
    """Generate `count` unique student IDs in YYYY-NNNN format."""
    years = list(range(2018, 2026))
    generated = set()
    result = []

    attempts = 0
    max_attempts = count * 20

    while len(result) < count and attempts < max_attempts:
        attempts += 1
        year = random.choice(years)
        number = random.randint(1000, 9999)
        student_id = f"{year}-{number}"
        if student_id not in existing_ids and student_id not in generated:
            generated.add(student_id)
            result.append(student_id)

    if len(result) < count:
        raise RuntimeError(
            f"Could only generate {len(result)} unique IDs after {max_attempts} attempts. "
            "Try clearing some existing students first."
        )

    return result


def seed():
    db = get_db()
    cur = db.cursor(dictionary=True)

    # ── Fetch available course codes ──
    cur.execute("SELECT course_code FROM course")
    course_rows = cur.fetchall()
    if not course_rows:
        print("ERROR: No courses found in the database.")
        print("Please add at least one college and course before seeding students.")
        cur.close()
        db.close()
        return

    course_codes = [r["course_code"] for r in course_rows]
    print(f"Found {len(course_codes)} course(s): {', '.join(course_codes)}")

    # ── Fetch existing student IDs to avoid duplicates ──
    cur.execute("SELECT student_id FROM student")
    existing_ids = {r["student_id"] for r in cur.fetchall()}
    print(f"Existing students in DB: {len(existing_ids)}")

    # ── Generate unique IDs ──
    TARGET = 1500
    needed = max(0, TARGET - len(existing_ids))
    if needed == 0:
        print(f"Already have {len(existing_ids)} students. Nothing to insert.")
        cur.close()
        db.close()
        return

    print(f"Generating {needed} new student(s)...")
    new_ids = generate_unique_ids(existing_ids, needed)

    # ── Build and insert rows ──
    genders = ["Male", "Female"]
    year_levels = [1, 2, 3, 4]

    rows = []
    for student_id in new_ids:
        rows.append((
            student_id,
            random.choice(FIRST_NAMES),
            random.choice(LAST_NAMES),
            random.choice(course_codes),
            random.choice(year_levels),
            random.choice(genders),
            None,  # student_url
        ))

    cur.executemany("""
        INSERT INTO student
            (student_id, first_name, last_name, course_code, year_level, gender, student_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, rows)

    db.commit()
    print(f"Done! Inserted {len(rows)} student(s). Total in DB: {len(existing_ids) + len(rows)}")

    cur.close()
    db.close()


if __name__ == "__main__":
    seed()
