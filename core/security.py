import hashlib
import re

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^07\d{8}$", phone))

def validate_mac(mac: str) -> bool:
    return bool(re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac))