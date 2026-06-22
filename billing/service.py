import secrets
import string
from datetime import datetime, timedelta

from billing.plans import get_plan, get_plan_duration, get_mikrotik_profile
from billing.transactions import save_transaction, get_transaction, update_transaction
from core.session_manager import create_session
from mikrotik.hotspot_users import create_hotspot_user
from utils.logger import log_payment, log_system, audit_transaction


SUCCESS_STATES = {
    "success",
    "completed",
    "paid",
    "confirmed"
}

FAILURE_STATES = {
    "failed",
    "cancelled",
    "rejected",
    "declined"
}


def normalize_phone(phone):
    if not phone:
        return None

    phone = phone.strip()

    if phone.startswith("07"):
        return "254" + phone[1:]

    if phone.startswith("+"):
        return phone[1:]

    return phone


def generate_txn_id():
    stamp = int(datetime.utcnow().timestamp() * 1000)
    suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"TXN{stamp}{suffix}"


def create_guest_transaction(phone, plan_id, mac=None):
    plan = get_plan(plan_id)
    if not plan:
        return {
            "success": False,
            "message": "Invalid plan selected"
        }

    phone = normalize_phone(phone)
    if not phone:
        return {
            "success": False,
            "message": "Invalid phone number"
        }

    txn_id = generate_txn_id()
    amount = plan["price"]

    saved = save_transaction({
        "phone": phone,
        "plan": plan_id,
        "amount": amount,
        "status": "pending",
        "mac": mac,
        "created_at": datetime.utcnow()
    }, txn_id=txn_id)

    if not saved:
        return {
            "success": False,
            "message": "Unable to save transaction"
        }

    log_payment(f"Transaction created {txn_id} for {phone} / {plan_id}")
    audit_transaction(
        txn_id=txn_id,
        action="created",
        new_value=f"pending",
        field_name="status",
        reason=f"Guest initiated payment for plan {plan_id}"
    )

    return {
        "success": True,
        "txn_id": txn_id,
        "phone": phone,
        "plan": plan_id,
        "amount": amount
    }


def should_mark_success(status):
    if not status:
        return False
    return str(status).lower() in SUCCESS_STATES


def should_mark_failed(status):
    if not status:
        return False
    return str(status).lower() in FAILURE_STATES


def build_mikrotik_credentials(txn_id):
    username = f"guest_{txn_id[-8:]}"
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
    return username, password


def activate_transaction(txn, receipt=None, provider_status=None, phone=None, amount=None):
    if not txn:
        return {
            "success": False,
            "message": "Transaction missing"
        }

    plan_id = txn.get("plan")
    mac = txn.get("mac")
    phone = phone or txn.get("phone")
    amount = amount if amount is not None else txn.get("amount")

    duration = get_plan_duration(plan_id) or 3600
    expiry = datetime.utcnow() + timedelta(seconds=duration)
    username, password = build_mikrotik_credentials(txn.get("id"))
    profile = get_mikrotik_profile(plan_id)

    mikrotik_result = None
    if profile:
        mikrotik_result = create_hotspot_user(username, password, profile)

    if mac:
        create_session(mac, phone, duration)
        log_system(f"Session created for {mac} until {expiry.isoformat()}")

    update_data = {
        "status": "success",
        "paid_at": datetime.utcnow(),
        "expiry": expiry,
        "active": 1,
        "phone": phone,
        "amount": amount,
        "mikrotik_username": username,
        "mikrotik_password": password
    }

    if provider_status is not None:
        update_data["status"] = "success" if should_mark_success(provider_status) else "failed"

    if receipt:
        update_data["mpesa_receipt"] = receipt

    if mikrotik_result is not None:
        update_data["mikrotik_status"] = mikrotik_result.get("status")
        update_data["mikrotik_message"] = mikrotik_result.get("message")

    success = update_transaction(txn.get("id"), update_data)

    if not success:
        return {
            "success": False,
            "message": "Failed to update transaction"
        }

    # Audit log the activation
    audit_transaction(
        txn_id=txn.get("id"),
        action="activated",
        old_value="pending",
        new_value="success",
        field_name="status",
        reason=f"Payment confirmed via webhook, receipt={receipt}, provider_status={provider_status}"
    )

    return {
        "success": True,
        "transaction_id": txn.get("id"),
        "mikrotik": mikrotik_result,
        "expiry": expiry.isoformat()
    }


def handle_webhook_payload(payload):
    txn_id = payload.get("transactionId") or payload.get("reference") or payload.get("txn_id")
    status = payload.get("status")
    phone = payload.get("phone")
    amount = payload.get("amount")
    receipt = payload.get("receipt") or payload.get("mpesa_receipt") or payload.get("transactionCode")

    if not txn_id:
        return {
            "success": False,
            "message": "Missing transaction ID"
        }

    txn = get_transaction(txn_id)
    if not txn:
        log_system(f"Webhook could not find transaction: {txn_id}")
        return {
            "success": False,
            "message": "Transaction not found"
        }

    if should_mark_success(status):
        return activate_transaction(txn, receipt=receipt, provider_status=status, phone=phone, amount=amount)

    if should_mark_failed(status):
        update_transaction(txn_id, {"status": "failed"})
        audit_transaction(
            txn_id=txn_id,
            action="failed",
            old_value="pending",
            new_value="failed",
            field_name="status",
            reason=f"Payment failed via webhook, provider_status={status}"
        )
        return {
            "success": True,
            "message": "Marked transaction failed"
        }

    return {
        "success": True,
        "message": "Webhook received, transaction remains pending"
    }
