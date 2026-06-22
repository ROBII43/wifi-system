from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash
)

import time
import random
import string
from datetime import datetime

from billing.plans import get_plan_price
from billing.transactions import (
    get_transaction,
    update_transaction
)
from billing.lipana import initiate_stk_push
from billing.service import (
    activate_transaction,
    create_guest_transaction
)

payments_bp = Blueprint("payments", __name__)


def serialize_transaction(txn):
    if not txn:
        return None

    sensitive_fields = {
        "mpesa_receipt",
        "mikrotik_password",
        "mikrotik_message"
    }

    serialized = {}
    for key, value in txn.items():
        if key in sensitive_fields:
            continue

        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value

    return serialized


# ---------------------------------------------------
# PAY
# ---------------------------------------------------
@payments_bp.route("/pay", methods=["POST"])
def pay():

    phone = request.form.get("phone", "").strip()
    plan = request.form.get("plan", "").strip()
    mac = request.form.get("mac", "").strip()

    if not phone or not plan:
        flash("Phone and plan required", "danger")
        return redirect(url_for("portal.login_page"))

    result = create_guest_transaction(phone, plan, mac=mac)
    if not result.get("success"):
        flash(result.get("message", "Unable to start payment"), "danger")
        return redirect(url_for("portal.login_page"))

    txn_id = result["txn_id"]
    phone = result["phone"]
    amount = result["amount"]

    print("🔥 TXN:", txn_id)

    try:
        stk = initiate_stk_push(
            phone=phone,
            amount=amount,
            reference=txn_id
        )

        if not stk.get("success"):
            update_transaction(txn_id, {"status": "failed"})
            return render_template("payment_failed.html", error=stk.get("message", "STK failed"))

    except Exception as e:
        update_transaction(txn_id, {"status": "failed"})
        return render_template("payment_failed.html", error=str(e))

    return render_template(
        "payment_pending.html",
        txn_id=txn_id,
        phone=phone,
        plan=plan
    )


# ---------------------------------------------------
# STATUS CHECK
# ---------------------------------------------------
@payments_bp.route("/pay/status/<txn_id>")
def payment_status(txn_id):

    if not txn_id or txn_id == "None":
        return jsonify({
            "success": False,
            "message": "Invalid transaction ID"
        }), 400

    txn = get_transaction(txn_id)

    if not txn:
        return jsonify({
            "success": False,
            "message": "Transaction not found"
        }), 404

    return jsonify({
        "success": True,
        "transaction": serialize_transaction(txn)
    })


# ---------------------------------------------------
# VERIFY CODE
# ---------------------------------------------------
@payments_bp.route("/pay/verify-code", methods=["POST"])
def verify_code():

    data = request.get_json()

    txn_id = data.get("txn_id", "").strip()
    code = data.get("code", "").strip().upper()

    txn = get_transaction(txn_id)

    if not txn:
        return jsonify({"success": False, "message": "Transaction not found"}), 404

    if len(code) < 6:
        return jsonify({"success": False, "message": "Invalid code"}), 400

    result = activate_transaction(
        txn,
        receipt=code,
        provider_status="confirmed"
    )

    if not result.get("success"):
        return jsonify({
            "success": False,
            "message": result.get("message", "Failed to activate payment")
        }), 500

    return jsonify({
        "success": True,
        "message": "Payment verified"
    })


# ---------------------------------------------------
# SUCCESS PAGE (FIXED ROUTE)
# ---------------------------------------------------
@payments_bp.route("/pay/success")
def success():

    txn_id = request.args.get("txn_id")

    txn = get_transaction(txn_id) if txn_id else None

    return render_template("payment_success.html", txn=txn)


# ---------------------------------------------------
# FAILED PAGE
# ---------------------------------------------------
@payments_bp.route("/pay/failed")
def failed():
    return render_template("payment_failed.html")