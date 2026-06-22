from flask import render_template, request
from . import admin_bp

USERS = []


@admin_bp.route("/users")
def users():
    return render_template("admin/users.html", users=USERS)


@admin_bp.route("/users/add", methods=["POST"])
def add_user():

    user = {
        "name": request.form.get("name"),
        "phone": request.form.get("phone"),
        "plan": request.form.get("plan")
    }

    USERS.append(user)

    return {"status": "user_added"}