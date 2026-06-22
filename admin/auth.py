from flask import Blueprint, render_template, request, redirect, session, url_for
import mysql.connector
import hashlib

admin_auth_bp = Blueprint("admin_auth", __name__)

# DB connection helper
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NewPassword123!",
        database="wifi_system"
    )

# Hash function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@admin_auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admins WHERE username=%s AND password=%s",
            (username, hash_password(password))
        )

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin:
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin.dashboard"))

        return "Invalid credentials", 401

    return render_template("admin_login.html")


@admin_auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_auth.login"))