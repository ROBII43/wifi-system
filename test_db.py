from database.connection import get_db_connection

try:

    conn = get_db_connection()

    print("✅ MYSQL CONNECTED")

    conn.close()

except Exception as e:

    print("❌ ERROR:", e)