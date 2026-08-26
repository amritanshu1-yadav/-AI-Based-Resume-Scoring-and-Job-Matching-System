import sqlite3


DATABASE = "resume_matcher.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_name TEXT,

            job_title TEXT,

            score REAL,

            skill_score REAL,

            similarity_score REAL,

            matched_skills TEXT,

            missing_skills TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


def save_analysis(
    resume_name,
    job_title,
    score,
    skill_score,
    similarity_score,
    matched_skills,
    missing_skills
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (
            resume_name,
            job_title,
            score,
            skill_score,
            similarity_score,
            matched_skills,
            missing_skills
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_name,
        job_title,
        score,
        skill_score,
        similarity_score,
        matched_skills,
        missing_skills
    ))

    connection.commit()

    connection.close()


def get_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data