import os, psycopg2
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')


def connect_psql():
    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

    return psycopg2.connect(DATABASE_URL)


def add_lesson(title, content, file_id, file_type):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO lessons (title, content, file_id, file_type)
                VALUES (%s, %s, %s, %s)
            """, (title, content, file_id, file_type))
        conn.commit()
    finally:
        conn.close()


def get_lesson_by_id(lesson_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT title, content, file_id, file_type
                FROM lessons
                WHERE id = %s
            """, (lesson_id,))
            return cursor.fetchone()
    finally:
        conn.close()

def delete_lesson_by_id(l_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM lessons WHERE id = %s;", (l_id,))
        conn.commit()
    finally:
        conn.close()



"""---------------------Admin------------------"""

def get_admin():
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins;")
            return cursor.fetchall()
    finally:
        conn.close()


def check_admin(tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM admins WHERE tg_id = %s;", (tg_id,))
            return cursor.fetchone()  # mavjud bo‘lsa: (1,), yo‘q bo‘lsa: None
    finally:
        conn.close()


def add_admin_sql(name, username, tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO admins (name, username, tg_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (tg_id) DO NOTHING;
            """, (name, username, tg_id))
        conn.commit()
    finally:
        conn.close()


def delete_admin_sql(tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admins WHERE tg_id = %s;", (tg_id,))
        conn.commit()
    finally:
        conn.close()
