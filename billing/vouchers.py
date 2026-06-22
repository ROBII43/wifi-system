import random
import string
from utils.logger import log_system, log_user

VOUCHERS = {}


# ---------------------------------------------------
# GENERATE VOUCHER
# ---------------------------------------------------
def generate_voucher(plan, created_by="admin"):

    code = ''.join(random.choices(
        string.ascii_uppercase + string.digits,
        k=10
    ))

    VOUCHERS[code] = {
        "plan": plan,
        "used": False
    }

    log_system(f"Voucher generated: {code} | Plan: {plan}")
    log_user(f"Voucher created by {created_by}: {code}")

    return code


# ---------------------------------------------------
# REDEEM VOUCHER
# ---------------------------------------------------
def redeem_voucher(code):

    voucher = VOUCHERS.get(code)

    if not voucher:
        log_system(f"Invalid voucher attempt: {code}", "WARNING")
        return None

    if voucher["used"]:
        log_system(f"Voucher already used: {code}", "WARNING")
        return None

    voucher["used"] = True

    log_user(f"Voucher redeemed: {code} | Plan: {voucher['plan']}")
    log_system(f"Voucher activated: {code}")

    return voucher["plan"]


# ---------------------------------------------------
# GET ALL VOUCHERS (ADMIN)
# ---------------------------------------------------
def get_vouchers():
    return VOUCHERS