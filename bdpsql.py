import psycopg2
from config import DB_CONFIG as dbs
def db_connection():
    conn = psycopg2.connect(
        dbname=dbs["dbname"],
        user=dbs["user"],
        password=dbs["password"],
        host=dbs["host"],  # або інший хост
        port=dbs["port"]  # стандартний порт PostgreSQL
    )
    return conn

# Створюємо таблицю для нагадувань
def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            reminder_text TEXT,
            reminder_time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
