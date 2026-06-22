from database.connection import get_db_connection


class User:

    @staticmethod
    def create(phone, mac, plan, expiry):

        conn = get_db_connection()

        try:
            with conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO users
                    (phone, mac, plan, expiry, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    phone,
                    mac,
                    plan,
                    expiry,
                    "active"
                ))

            conn.commit()
            print("✅ USER CREATED:", mac)

        except Exception as e:
            print("❌ USER CREATE ERROR:", str(e))
            conn.rollback()

        finally:
            conn.close()


    @staticmethod
    def get_by_mac(mac):

        conn = get_db_connection()

        try:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT *
                    FROM users
                    WHERE mac=%s
                    LIMIT 1
                """, (mac,))

                user = cur.fetchone()

                if user:
                    print("✅ USER FOUND:", mac)
                else:
                    print("❌ USER NOT FOUND:", mac)

                return user

        except Exception as e:
            print("❌ USER FETCH ERROR:", str(e))
            return None

        finally:
            conn.close()


    @staticmethod
    def get_all():

        conn = get_db_connection()

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM users
                    ORDER BY expiry DESC
                """)
                users = cur.fetchall()
                print("📦 USERS LOADED:", len(users))
                return users

        except Exception as e:
            print("❌ USERS LIST ERROR:", str(e))
            return []

        finally:
            conn.close()