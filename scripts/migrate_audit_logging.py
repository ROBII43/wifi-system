#!/usr/bin/env python
"""
Migration: Add audit logging table to track transaction state changes
"""
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def migrate():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    try:
        with conn.cursor() as cur:
            # Create audit_log table if it doesn't exist
            sql = """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_id VARCHAR(100),
                action VARCHAR(50),
                old_status VARCHAR(20),
                new_status VARCHAR(20),
                field_changed VARCHAR(100),
                old_value TEXT,
                new_value TEXT,
                user_id VARCHAR(100),
                ip_address VARCHAR(50),
                reason TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_txn (transaction_id),
                INDEX idx_action (action),
                INDEX idx_created (created_at)
            )
            """
            cur.execute(sql)
            print("✅ audit_log table created/verified")

        conn.commit()
        print("✅ Migration successful")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
