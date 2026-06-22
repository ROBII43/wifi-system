# billing/plans.py
# ISP pricing definitions (single source of truth)

PLANS = {
    "hourly": {
        "name": "1 Hour Plan",
        "price": 10,
        "duration": 3600,  # seconds
        "mikrotik_profile": "1M"
    },

    "daily": {
        "name": "Daily Plan",
        "price": 20,
        "duration": 86400,  # 24 hours
        "mikrotik_profile": "2M"
    },

    "weekly": {
        "name": "Weekly Plan",
        "price": 100,
        "duration": 604800,  # 7 days
        "mikrotik_profile": "5M"
    }
}


# ---------------------------------------------------
# GET FULL PLAN OBJECT
# ---------------------------------------------------
def get_plan(plan_id):
    return PLANS.get(plan_id)


# ---------------------------------------------------
# GET PRICE ONLY
# ---------------------------------------------------
def get_plan_price(plan_id):
    plan = PLANS.get(plan_id)
    return plan["price"] if plan else None


# ---------------------------------------------------
# GET DURATION (SECONDS)  ✅ USED BY WEBHOOK
# ---------------------------------------------------
def get_plan_duration(plan_id):
    plan = PLANS.get(plan_id)
    return plan["duration"] if plan else 0


# ---------------------------------------------------
# GET MICROTIK PROFILE (FOR ISP AUTO ACTIVATION)
# ---------------------------------------------------
def get_mikrotik_profile(plan_id):
    plan = PLANS.get(plan_id)
    return plan["mikrotik_profile"] if plan else None