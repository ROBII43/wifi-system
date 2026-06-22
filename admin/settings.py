from flask import render_template, request, session, redirect, url_for
from config import Config
from . import admin_bp


@admin_bp.route("/settings", methods=["GET", "POST"])
def settings():

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    message = None
    error = None

    if request.method == "POST":
        try:
            Config.MIKROTIK_HOST = request.form.get("mikrotik_ip")
            Config.MIKROTIK_USER = request.form.get("username")
            Config.MIKROTIK_PASSWORD = request.form.get("password")
            session_time = request.form.get("session_time")

            if session_time:
                Config.SESSION_DURATION = int(session_time)

            message = "Settings updated successfully."
        except Exception as exc:
            error = f"Unable to save settings: {exc}"

    return render_template(
        "admin_settings.html",
        settings=Config,
        message=message,
        error=error
    )