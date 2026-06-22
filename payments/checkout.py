from billing.lipana import initiate_stk_push
from billing.service import create_guest_transaction

# ---------------------------------------------------
# INITIATE PAYMENT
# ---------------------------------------------------
def initiate_payment(phone, plan_id, mac=None):
    result = create_guest_transaction(phone, plan_id, mac=mac)
    if not result.get('success'):
        return result

    try:
        stk_response = initiate_stk_push(
            phone=result['phone'],
            amount=result['amount'],
            reference=result['txn_id']
        )

        if not stk_response.get('success'):
            return {
                'success': False,
                'message': stk_response.get('message', 'STK push failed')
            }

        return {
            'success': True,
            'txn_id': result['txn_id'],
            'phone': result['phone'],
            'plan': result['plan'],
            'amount': result['amount'],
            'response': stk_response
        }

    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
