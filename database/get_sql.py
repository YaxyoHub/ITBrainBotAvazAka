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

def get_admins():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM admins;")
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    return data

def get_user():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users;")
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    return data

def check_user(id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id = %s;", (id,))
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    return data

def get_lesson():
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title FROM lessons ORDER BY id;")
            return cursor.fetchall()  # [(1, "Python"), (2, "Django")]
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
            return cursor.fetchone()  # (title, content, file_id, file_type)
    finally:
        conn.close()



"""+------------------User------------------+"""


def add_user(name, username, tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (name, username, tg_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (tg_id) DO NOTHING;
            """, (name, username, tg_id))
        conn.commit()
    finally:
        conn.close()


def delete_user(tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE tg_id = %s;", (tg_id,))
        conn.commit()
    finally:
        conn.close()


def check_user(tg_id):
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM users WHERE tg_id = %s;", (tg_id,))
            return cursor.fetchone()  # mavjud bo‘lsa (1,), yo‘q bo‘lsa None
    finally:
        conn.close()


def get_all_users():
    conn = connect_psql()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY id;")
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_users_id():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM users;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return [u[0] for u in users]
