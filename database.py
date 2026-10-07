import sqlite3
from datetime import datetime

DATABASE = "attendance.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            department TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Present'
        )
    """)

    conn.commit()
    conn.close()


def add_student(student_id, name, email, department):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (student_id, name, email, department, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            email,
            department,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def get_students():

    conn = get_connection()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return students


def get_student(student_id):

    conn = get_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE student_id = ?
    """, (student_id,)).fetchone()

    conn.close()

    return student


def mark_attendance(student_id, name):

    conn = get_connection()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    existing = conn.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        AND date = ?
    """, (student_id, today)).fetchone()

    if existing:

        conn.close()

        return False

    conn.execute("""
        INSERT INTO attendance
        (student_id, name, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        name,
        today,
        current_time,
        "Present"
    ))

    conn.commit()
    conn.close()

    return True


def get_attendance():

    conn = get_connection()

    attendance = conn.execute("""
        SELECT *
        FROM attendance
        ORDER BY date DESC, time DESC
    """).fetchall()

    conn.close()

    return attendance


def get_attendance_by_date(date):

    conn = get_connection()

    attendance = conn.execute("""
        SELECT *
        FROM attendance
        WHERE date = ?
        ORDER BY time DESC
    """, (date,)).fetchall()

    conn.close()

    return attendance