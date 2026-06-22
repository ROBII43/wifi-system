import os
import datetime
from database.connection import get_db_connection

LOG_DIR = "logs"

SYSTEM_LOG = os.path.join(LOG_DIR, "system.log")
USER_LOG = os.path.join(LOG_DIR, "users.log")
PAYMENT_LOG = os.path.join(LOG_DIR, "payments.log")


def _write(file_path, message, level="INFO"):
    os.makedirs(LOG_DIR, exist_ok=True)

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{time}] [{level}] {message}\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(line)


# -------------------------
# SYSTEM LOGS
# -------------------------
def log_system(message, level="INFO"):
    _write(SYSTEM_LOG, message, level)


# -------------------------
# USER LOGS
# -------------------------
def log_user(message, level="USER"):
    _write(USER_LOG, message, level)


# -------------------------
# PAYMENT LOGS
# -------------------------
def log_payment(message, level="PAYMENT"):
    _write(PAYMENT_LOG, message, level)


# -------------------------
# AUDIT LOGS (DATABASE)
# -------------------------
def audit_transaction(txn_id, action, old_value=None, new_value=None, field_name=None, reason=None, user_id=None, ip_address=None):
    """
    Log transaction state changes to database for audit trail.
    
    Args:
        txn_id: Transaction ID
        action: Action type (e.g., 'created', 'status_changed', 'activated', 'failed')
        old_value: Previous value (optional)
        new_value: New value (optional)
        field_name: Field that changed (optional, e.g., 'status', 'amount')
        reason: Reason for change (optional)
        user_id: User performing action (optional)
        ip_address: Client IP (optional)
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = """
            INSERT INTO audit_log 
            (transaction_id, action, old_value, new_value, field_changed, reason, user_id, ip_address, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                txn_id,
                action,
                str(old_value)[:255] if old_value else None,
                str(new_value)[:255] if new_value else None,
                field_name,
                reason,
                user_id,
                ip_address,
                datetime.datetime.utcnow()
            )
            cur.execute(sql, values)
        conn.commit()
        conn.close()
        log_system(f"AUDIT: {txn_id} / {action} / {field_name}", "AUDIT")
    except Exception as e:
        log_system(f"AUDIT ERROR: {txn_id} / {str(e)}", "ERROR")


def get_audit_log(txn_id):
    """Retrieve all audit logs for a transaction"""
    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT * FROM audit_log 
                WHERE transaction_id=%s 
                ORDER BY created_at DESC
            """, (txn_id,))
            rows = cur.fetchall()
        conn.close()
        return rows or []
    except Exception as e:
        log_system(f"AUDIT FETCH ERROR: {str(e)}", "ERROR")
        return []
