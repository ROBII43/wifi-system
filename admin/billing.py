from flask import render_template
from . import admin_bp
from billing.transactions import get_all_transactions


@admin_bp.route("/billing")
def billing():

    transactions = get_all_transactions() or []

    revenue = sum(float(t.get("amount", 0)) for t in transactions if t.get("status") == "success")
    pending = sum(1 for t in transactions if t.get("status") not in ("success", "failed"))

    return render_template(
        "admin_billing.html",
        transactions=transactions,
        revenue=revenue,
        pending=pending
    )