import requests
from config import Config


def initiate_stk_push(phone, amount, reference=None):

    url = "https://api.lipana.dev/v1/transactions/push-stk"

    headers = {
        "x-api-key": Config.LIPANA_SECRET_KEY,
        "Content-Type": "application/json"
    }

    # ---------------------------------------------------
    # USE YOUR OWN TXN ID
    # ---------------------------------------------------
    payload = {
        "phone": phone,
        "amount": amount,
        "reference": reference,
        "callback_url": Config.LIPANA_CALLBACK_URL
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        print("📡 STATUS:", response.status_code)
        print("📡 RESPONSE:", response.text)

        response.raise_for_status()

        data = response.json()

        # ---------------------------------------------------
        # FORCE SYSTEM CONSISTENCY
        # ---------------------------------------------------
        return {
            "success": True,
            "transactionId": reference,
            "provider_transaction": (
                data.get("data", {}).get("transactionId")
            ),
            "status": (
                data.get("data", {}).get("status", "pending")
            ),
            "message": (
                data.get("message", "STK push initiated")
            ),
            "raw": data
        }

    except requests.exceptions.RequestException as e:

        print("❌ STK ERROR:", str(e))

        return {
            "success": False,
            "message": str(e),
            "raw": (
                getattr(e, "response", None).text
                if getattr(e, "response", None)
                else None
            )
        }