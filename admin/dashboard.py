from flask import Blueprint, render_template, session, redirect
from billing.transactions import get_all_transactions

admin_bp = Blueprint("admin", __name__)


def dashboard_data():
    transactions = get_all_transactions() or []

    revenue = 0
    successful = 0
    pending = 0
    failed = 0

    for t in transactions:
        status = t.get("status", "")

        try:
            amount = float(t.get("amount", 0))
        except:
            amount = 0

        if status == "success":
            revenue += amount
            successful += 1
        elif status == "pending":
            pending += 1
        elif status == "failed":
            failed += 1

    return {
        "revenue": revenue,
        "total_transactions": len(transactions),
        "successful": successful,
        "pending": pending,
        "failed": failed,
        "transactions": transactions
    }


@admin_bp.route("/")
def dashboard():

    if not session.get("admin_logged_in"):
        return redirect("/admin_login")

    data = dashboard_data()

    return render_template("admin_dashboard.html", data=data)