from flask import render_template

def render_login():
    return render_template("login.html")

def render_success():
    return render_template("success.html")