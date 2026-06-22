import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

ALTER_STATEMENTS = [
    "ALTER TABLE transactions ADD COLUMN expiry DATETIME NULL;",
    "ALTER TABLE transactions ADD COLUMN mikrotik_username VARCHAR(100) NULL;",
    "ALTER TABLE transactions ADD COLUMN mikrotik_password VARCHAR(100) NULL;",
    "ALTER TABLE transactions ADD COLUMN mikrotik_status VARCHAR(50) NULL;",
    "ALTER TABLE transactions ADD COLUMN mikrotik_message TEXT NULL;",
]


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=False,
        connection_timeout=5,
    )


def column_exists(cursor, table_name, column_name):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema=%s AND table_name=%s AND column_name=%s",
        (DB_NAME, table_name, column_name),
    )
    return cursor.fetchone()[0] > 0


def migrate_transactions_table():
    print("🚀 Starting transactions schema migration", flush=True)
    try:
        with get_connection() as conn:
            print(f"🔌 Connected to {DB_NAME}@{DB_HOST}", flush=True)
            with conn.cursor() as cursor:
                for statement in ALTER_STATEMENTS:
                    column_name = statement.split(" ")[6]
                    if column_exists(cursor, "transactions", column_name):
                        print(f"✅ Column already exists: {column_name}", flush=True)
                        continue

                    try:
                        print(f"⚙️ Applying: {statement}", flush=True)
                        cursor.execute(statement)
                        conn.commit()
                        print(f"✅ Added column: {column_name}", flush=True)
                    except mysql.connector.Error as ex:
                        print(f"❌ Failed to add {column_name}: {ex}", flush=True)
                        conn.rollback()

        print("✅ Migration complete", flush=True)
    except Exception as ex:
        print(f"❌ Migration failed: {type(ex).__name__}: {ex}", flush=True)


if __name__ == "__main__":
    migrate_transactions_table()
