from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from mikrotik.client import connect
from utils.logger import log_user, log_system

mikrotik_bp = Blueprint("mikrotik", __name__)


# ---------------------------------------------------
# ADMIN AUTH
# ---------------------------------------------------
def admin_required():
    return session.get("admin") is True


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
@mikrotik_bp.route("/")
def mikrotik_dashboard():

    if not admin_required():
        return redirect(url_for("admin.login"))

    status = "Disconnected"

    try:
        api = connect()
        identity = api.get_resource("/system/identity").get()

        if identity:
            status = "Connected"
            log_system("MikroTik connection successful")

    except Exception as e:
        status = "Connection Failed"
        log_system(f"MikroTik connection failed: {str(e)}", "ERROR")

    return render_template("admin/mikrotik.html", status=status)


# ---------------------------------------------------
# CREATE HOTSPOT USER
# ---------------------------------------------------
@mikrotik_bp.route("/create-user", methods=["POST"])
def create_hotspot_user():

    if not admin_required():
        return redirect(url_for("admin.login"))

    username = request.form.get("username")
    password = request.form.get("password")
    profile = request.form.get("profile")

    try:
        api = connect()

        api.get_resource("/ip/hotspot/user").add(
            name=username,
            password=password,
            profile=profile
        )

        log_user(f"Hotspot user created: {username} | Profile: {profile}")

        flash("User created successfully", "success")

    except Exception as e:
        log_system(f"User creation failed: {str(e)}", "ERROR")
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("mikrotik.active_users"))


# ---------------------------------------------------
# ENABLE HOTSPOT
# ---------------------------------------------------
@mikrotik_bp.route("/enable")
def enable_hotspot():

    if not admin_required():
        return redirect(url_for("admin.login"))

    try:
        api = connect()
        hotspot = api.get_resource("/ip/hotspot")

        for h in hotspot.get():
            hotspot.set(id=h[".id"], disabled="no")

        log_system("Hotspot enabled")
        flash("Hotspot enabled", "success")

    except Exception as e:
        log_system(f"Enable hotspot failed: {str(e)}", "ERROR")
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("mikrotik.mikrotik_dashboard"))


# ---------------------------------------------------
# DISABLE HOTSPOT
# ---------------------------------------------------
@mikrotik_bp.route("/disable")
def disable_hotspot():

    if not admin_required():
        return redirect(url_for("admin.login"))

    try:
        api = connect()
        hotspot = api.get_resource("/ip/hotspot")

        for h in hotspot.get():
            hotspot.set(id=h[".id"], disabled="yes")

        log_system("Hotspot disabled")
        flash("Hotspot disabled", "warning")

    except Exception as e:
        log_system(f"Disable hotspot failed: {str(e)}", "ERROR")
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("mikrotik.mikrotik_dashboard"))


# ---------------------------------------------------
# RESTART ROUTER
# ---------------------------------------------------
@mikrotik_bp.route("/restart")
def restart_router():

    if not admin_required():
        return redirect(url_for("admin.login"))

    try:
        api = connect()
        api.get_resource("/system/reboot").call("reboot")

        log_system("Router reboot triggered")
        flash("Router restarting...", "success")

    except Exception as e:
        log_system(f"Router restart failed: {str(e)}", "ERROR")
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("mikrotik.mikrotik_dashboard"))


# ---------------------------------------------------
# ACTIVE USERS
# ---------------------------------------------------
@mikrotik_bp.route("/active-users")
def active_users():

    if not admin_required():
        return redirect(url_for("admin.login"))

    users = []

    try:
        api = connect()
        users = api.get_resource("/ip/hotspot/active").get()

        log_system(f"Loaded active users: {len(users)}")

    except Exception as e:
        log_system(f"Failed to load active users: {str(e)}", "ERROR")
        flash(f"Error loading users: {str(e)}", "danger")

    return render_template("admin_active_users.html", users=users)