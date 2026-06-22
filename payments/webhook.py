from flask import Blueprint, request, jsonify
import json

from billing.service import handle_webhook_payload


webhook_bp = Blueprint("webhook", __name__)


# ---------------------------------------------------
# LIPANA WEBHOOK
# ---------------------------------------------------
@webhook_bp.route("/callback", methods=["POST"])
def lipana_webhook():

    try:

        # ---------------------------------------------------
        # RECEIVE JSON
        # ---------------------------------------------------
        data = request.get_json(force=True)

        print("\n🔥 WEBHOOK RECEIVED")
        print(json.dumps(data, indent=4))

        # ---------------------------------------------------
        # SUPPORT MULTIPLE FORMATS
        # ---------------------------------------------------
        payload = data.get("data", {}) or data

        print("🔍 WEBHOOK PAYLOAD:", payload)

        response = handle_webhook_payload(payload)
        status_code = 200 if response.get("success") else 400
        return jsonify(response), status_code

    except Exception as e:

        print("❌ WEBHOOK ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500