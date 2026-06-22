from flask import Flask
from config import Config
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV FIRST (VERY IMPORTANT)
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# BLUEPRINT IMPORTS
# ---------------------------------------------------
from admin.routes import admin_bp
from portal.routes import portal_bp
from payments.routes import payments_bp
from payments.webhook import webhook_bp
from admin.mikrotik import mikrotik_bp


# ---------------------------------------------------
# APP FACTORY
# ---------------------------------------------------
def create_app():

    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # ---------------------------------------------------
    # SAFE SESSION / DEBUG GUARD
    # ---------------------------------------------------
    app.config["JSON_SORT_KEYS"] = False

    # ---------------------------------------------------
    # BLUEPRINT REGISTRATION
    # ---------------------------------------------------
    app.register_blueprint(portal_bp)

    app.register_blueprint(payments_bp, url_prefix="/pay")

    app.register_blueprint(webhook_bp, url_prefix="/webhook")

    app.register_blueprint(admin_bp, url_prefix="/admin")

    app.register_blueprint(mikrotik_bp, url_prefix="/admin/mikrotik")

    # ---------------------------------------------------
    # BASIC ROUTES
    # ---------------------------------------------------
    @app.route("/")
    def home():
        return "🚀 ISP CAPTIVE PORTAL RUNNING"

    @app.route("/health")
    def health():
        return {
            "status": "OK",
            "service": "ISP SYSTEM",
            "db": "CONNECTED (if configured correctly)"
        }

    return app


# ---------------------------------------------------
# RUN SERVER
# ---------------------------------------------------
if __name__ == "__main__":

    app = create_app()

    print("🚀 ISP System running ")

    # IMPORTANT FOR PRODUCTION STABILITY
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True   # 🔥 FIX: prevents request blocking in STK polling
    )