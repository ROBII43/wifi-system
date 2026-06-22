from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from billing.transactions import get_all_transactions
from database.models import User
from billing.plans import get_plan_duration
from config import Config
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__)

# ----------------------------------------
# AUTH CHECK
# ----------------------------------------
# Uses environment-configured admin credentials
# ----------------------------------------
def admin_required():
    return session.get("admin") is True


# ----------------------------------------
# ROOT → DASHBOARD
# ----------------------------------------
@admin_bp.route("/")
def admin_index():
    return redirect(url_for("admin.dashboard"))


# ----------------------------------------
# LOGIN
# ----------------------------------------
ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    # already logged in
    if session.get("admin"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            session["admin_user"] = username

            return redirect(url_for("admin.dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")
# ----------------------------------------
# DASHBOARD
# ----------------------------------------
@admin_bp.route("/dashboard")
def dashboard():

    if not admin_required():
        return redirect(url_for("admin.login"))

    txns = get_all_transactions()

    data = {
        "revenue": sum(t.get("amount", 0) for t in txns if t.get("status") == "success"),
        "total_transactions": len(txns),
        "successful": len([t for t in txns if t.get("status") == "success"]),
        "pending": len([t for t in txns if t.get("status") == "pending"]),
        "failed": len([t for t in txns if t.get("status") == "failed"]),
        "transactions": txns
    }

    return render_template("admin_dashboard.html", data=data)


# ----------------------------------------
# USERS
# ----------------------------------------
@admin_bp.route("/users", methods=["GET", "POST"])
def users():

    if not admin_required():
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        phone = request.form.get("phone")
        mac = request.form.get("mac")
        plan = request.form.get("plan")

        if not phone or not mac or not plan:
            flash("Phone, MAC and plan are required", "danger")
            return redirect(url_for("admin.users"))

        duration = get_plan_duration(plan) or 3600
        expiry = datetime.utcnow() + timedelta(seconds=duration)

        User.create(phone, mac, plan, expiry)
        flash("Hotspot user record created", "success")
        return redirect(url_for("admin.users"))

    users = User.get_all()
    return render_template("admin_users.html", users=users)

# ----------------------------------------
# BILLING
# ----------------------------------------
@admin_bp.route("/billing")
def billing():

    if not admin_required():
        return redirect(url_for("admin.login"))

    txns = get_all_transactions()
    revenue = sum(t.get("amount", 0) for t in txns if t.get("status") == "success")
    pending = len([t for t in txns if t.get("status") == "pending"])
    failed = len([t for t in txns if t.get("status") == "failed"])
    success = len([t for t in txns if t.get("status") == "success"])

    return render_template(
        "admin_billing.html",
        transactions=txns,
        revenue=revenue,
        pending=pending,
        failed=failed,
        success=success
    )


# ----------------------------------------
# LOGS
# ----------------------------------------
@admin_bp.route("/logs")
def logs():

    if not admin_required():
        return redirect(url_for("admin.login"))

    logs_data = []

    try:
        with open("logs/system.log", "r", encoding="utf-8") as f:
            for line in f:
                text = line.strip()
                if not text:
                    continue
                level = "system"
                if "[PAYMENT]" in text:
                    level = "payments"
                elif "[USER]" in text:
                    level = "users"
                elif "[ERROR]" in text or "ERROR" in text:
                    level = "danger"

                logs_data.append({
                    "type": level,
                    "text": text
                })
    except FileNotFoundError:
        logs_data = [{"type": "system", "text": "No logs available"}]

    return render_template("admin_logs.html", logs=logs_data)


# ----------------------------------------
# TROUBLESHOOTING
# ----------------------------------------
@admin_bp.route("/troubleshooting")
def troubleshooting():

    if not admin_required():
        return redirect(url_for("admin.login"))

    issues = [
        "Check MikroTik connection",
        "Check internet gateway",
        "Check DNS resolution",
        "Check user session expiry",
        "Check billing system",
        "Check STK Push integration"
    ]

    return render_template("admin_troubleshooting.html", issues=issues)


# ----------------------------------------
# LOGOUT
# ----------------------------------------
@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))