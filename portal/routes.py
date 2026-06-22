from flask import Blueprint, render_template, request, redirect, url_for, flash

from payments.checkout import initiate_payment
from portal.auth import validate_login
from utils.logger import log_system, log_payment

portal_bp = Blueprint("portal", __name__)


# ---------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------
@portal_bp.route("/")
def login_page():
    return render_template("login.html")


# ---------------------------------------------------
# PAYMENT HANDLER (STK PUSH)
# ---------------------------------------------------
@portal_bp.route("/pay", methods=["POST"])
def pay():

    phone = request.form.get("phone")
    plan = request.form.get("plan")

    print("PHONE:", phone)
    print("PLAN:", plan)

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if not phone or not plan:
        flash("Missing phone or plan", "danger")
        return redirect(url_for("portal.login_page"))

    # -----------------------------
    # NORMALIZE PHONE (FIXED)
    # -----------------------------
    if phone.startswith("0"):
        phone = "254" + phone[1:]

    # -----------------------------
    # VALIDATE USER
    # -----------------------------
    if not validate_login(phone):
        log_system(f"Invalid login attempt: {phone}", "WARNING")
        flash("Invalid phone number", "danger")
        return redirect(url_for("portal.login_page"))

    # -----------------------------
    # INITIATE PAYMENT
    # -----------------------------
    try:
        stk_response = initiate_payment(phone, plan)

        log_payment(f"STK Push sent | {phone} | {plan}")
        log_system(f"Payment initiated: {phone}")

        if not stk_response.get("success"):
            flash(stk_response.get("message", "Payment initiation failed"), "danger")
            return redirect(url_for("portal.login_page"))

        txn_id = stk_response.get("txn_id")

        return render_template(
            "payment_pending.html",
            phone=phone,
            plan=plan,
            txn_id=txn_id,
            response=stk_response
        )

    except Exception as e:
        log_system(f"Payment error: {str(e)}", "ERROR")

        return render_template(
            "payment_failed.html",
            error=str(e)
        ), 500