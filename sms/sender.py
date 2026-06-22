import requests

API_URL = "https://sms-provider.example/send"

def send_sms(phone, message):
    payload = {
        "phone": phone,
        "message": message
    }

    try:
        requests.post(API_URL, json=payload)
        return True
    except:
        return False