import mysql.connector
from mysql.connector import Error
from config import Config


def get_db_connection():

    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=False,
            use_pure=True
        )

        print("🔌 DB CONNECTED:", Config.DB_NAME)
        return conn

    except Error as e:
        print("❌ DB CONNECTION FAILED:", str(e))
        raise
