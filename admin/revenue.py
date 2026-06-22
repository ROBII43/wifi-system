from billing.transactions import get_all_transactions

def calculate_revenue():
    txns = get_all_transactions()

    return sum(t["amount"] for t in txns if t["status"] == "success")