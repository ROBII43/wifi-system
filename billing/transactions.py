from database.connection import get_db_connection
from datetime import datetime


# ---------------------------------------------------
# SAVE TRANSACTION
# ---------------------------------------------------
def save_transaction(data, txn_id):

    conn = get_db_connection()

    try:

        print("🔥 SAVE START:", txn_id)

        with conn.cursor() as cur:

            sql = """
            INSERT INTO transactions
            (
                id,
                phone,
                plan,
                amount,
                status,
                mac,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # ---------------------------------------------------
            # SAFE VALUES
            # ---------------------------------------------------
            amount = data.get("amount", 0)

            created_at = data.get("created_at")

            if not created_at:
                created_at = datetime.utcnow()

            if isinstance(created_at, str):

                try:
                    created_at = datetime.fromisoformat(created_at)

                except:
                    created_at = datetime.utcnow()

            values = (
                txn_id,
                data.get("phone"),
                data.get("plan"),
                float(amount),
                data.get("status", "pending"),
                data.get("mac"),
                created_at
            )

            print("🔥 INSERT VALUES:", values)

            cur.execute(sql, values)

        conn.commit()

        print("✅ SAVE SUCCESS:", txn_id)

        return True

    except Exception as e:

        print("❌ SAVE FAILED:", repr(e))

        conn.rollback()

        return False

    finally:

        conn.close()


# ---------------------------------------------------
# GET TRANSACTION
# ---------------------------------------------------
def get_transaction(txn_id):

    conn = get_db_connection()

    try:

        with conn.cursor(dictionary=True) as cur:

            cur.execute("""
                SELECT *
                FROM transactions
                WHERE id=%s
                LIMIT 1
            """, (txn_id,))

            row = cur.fetchone()

            print(
                "🔍 LOOKUP:",
                txn_id,
                "=>",
                "FOUND" if row else "NOT FOUND"
            )

            return row

    except Exception as e:

        print("❌ GET ERROR:", repr(e))

        return None

    finally:

        conn.close()


# ---------------------------------------------------
# UPDATE TRANSACTION
# ---------------------------------------------------
def update_transaction(txn_id, updates):

    conn = get_db_connection()

    try:

        if not updates:

            print("⚠️ NO UPDATE DATA")

            return False

        fields = []
        values = []

        for key, value in updates.items():

            fields.append(f"{key}=%s")
            values.append(value)

        values.append(txn_id)

        sql = f"""
        UPDATE transactions
        SET {", ".join(fields)}
        WHERE id=%s
        """

        print("🔥 UPDATE SQL:", sql)
        print("🔥 UPDATE VALUES:", values)

        with conn.cursor() as cur:

            cur.execute(sql, values)

        conn.commit()

        print("✅ UPDATED:", txn_id)

        return True

    except Exception as e:

        print("❌ UPDATE ERROR:", repr(e))

        conn.rollback()

        return False

    finally:

        conn.close()


# ---------------------------------------------------
# MARK PAID
# ---------------------------------------------------
def mark_paid(txn_id, receipt=None):

    return update_transaction(txn_id, {
        "status": "success",
        "mpesa_receipt": receipt,
        "paid_at": datetime.utcnow(),
        "active": 1
    })


# ---------------------------------------------------
# GET ALL TRANSACTIONS
# ---------------------------------------------------
def get_all_transactions():

    conn = get_db_connection()

    try:

        with conn.cursor(dictionary=True) as cur:

            cur.execute("""
                SELECT *
                FROM transactions
                ORDER BY created_at DESC
            """)

            rows = cur.fetchall()

            print("📦 TOTAL TRANSACTIONS:", len(rows))

            return rows

    except Exception as e:

        print("❌ FETCH ERROR:", repr(e))

        return []

    finally:

        conn.close()


# ---------------------------------------------------
# GET SUCCESSFUL PAYMENTS
# ---------------------------------------------------
def get_successful_transactions():

    conn = get_db_connection()

    try:

        with conn.cursor(dictionary=True) as cur:

            cur.execute("""
                SELECT *
                FROM transactions
                WHERE status='success'
                ORDER BY created_at DESC
            """)

            rows = cur.fetchall()

            print("💰 SUCCESS PAYMENTS:", len(rows))

            return rows

    except Exception as e:

        print("❌ SUCCESS FETCH ERROR:", repr(e))

        return []

    finally:

        conn.close()


# ---------------------------------------------------
# DELETE TRANSACTION
# ---------------------------------------------------
def delete_transaction(txn_id):

    conn = get_db_connection()

    try:

        with conn.cursor() as cur:

            cur.execute("""
                DELETE FROM transactions
                WHERE id=%s
            """, (txn_id,))

        conn.commit()

        print("🗑️ DELETED:", txn_id)

        return True

    except Exception as e:

        print("❌ DELETE ERROR:", repr(e))

        conn.rollback()

        return False

    finally:

        conn.close()