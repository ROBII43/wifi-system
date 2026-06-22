from flask import jsonify
from . import admin_bp
from billing.transactions import get_all_transactions


@admin_bp.route("/api/stats")
def stats():

    tx = get_all_transactions() or []

    revenue = sum(float(t.get("amount", 0)) for t in tx if t.get("status") == "success")

    return jsonify({
        "revenue": revenue,
        "total": len(tx),
        "active_users": 10
    })