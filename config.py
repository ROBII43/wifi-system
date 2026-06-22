import os
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV FIRST
# ---------------------------------------------------
load_dotenv()


class Config:

    # ---------------------------------------------------
    # FLASK CORE
    # ---------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"

    # ---------------------------------------------------
    # MYSQL DATABASE
    # ---------------------------------------------------
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")

    # ❗ FORCE REQUIRED PASSWORD (NO SILENT FAIL)
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    if not DB_PASSWORD:
        raise Exception("❌ DB_PASSWORD missing in .env file")

    DB_NAME = os.getenv("DB_NAME", "wifi_system")

    # ---------------------------------------------------
    # LIPANA API
    # ---------------------------------------------------
    LIPANA_PUBLISHABLE_KEY = os.getenv("LIPANA_PUBLISHABLE_KEY")
    LIPANA_SECRET_KEY = os.getenv("LIPANA_SECRET_KEY")

    if not LIPANA_PUBLISHABLE_KEY or not LIPANA_SECRET_KEY:
        print("⚠️ WARNING: Lipana keys not set")

    # ---------------------------------------------------
    # CALLBACK URL
    # ---------------------------------------------------
    LIPANA_CALLBACK_URL = os.getenv(
        "LIPANA_CALLBACK_URL",
        "http://127.0.0.1:5000/webhook/callback"
    )

    # ---------------------------------------------------
    # MIKROTIK ROUTER SETTINGS
    # ---------------------------------------------------
    MIKROTIK_HOST = os.getenv("MIKROTIK_HOST")
    MIKROTIK_USER = os.getenv("MIKROTIK_USER")
    MIKROTIK_PASSWORD = os.getenv("MIKROTIK_PASSWORD")

    if not MIKROTIK_HOST or not MIKROTIK_USER or not MIKROTIK_PASSWORD:
        print("⚠️ WARNING: MikroTik credentials not fully configured")

    # ---------------------------------------------------
    # ADMIN CREDENTIALS
    # ---------------------------------------------------
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    if ADMIN_USERNAME == "admin" or ADMIN_PASSWORD == "admin123":
        print("⚠️ WARNING: using default admin credentials")

    # ---------------------------------------------------
    # WIFI DEFAULT SETTINGS
    # ---------------------------------------------------
    DEFAULT_PLAN = "hourly"
    DEFAULT_HOURS = 1

    # ---------------------------------------------------
    # SECURITY
    # ---------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"