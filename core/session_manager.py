import time

active_sessions = {}

def create_session(mac, phone, duration=3600):
    expiry = time.time() + duration

    active_sessions[mac] = {
        "phone": phone,
        "expiry": expiry,
        "active": True
    }

def is_session_active(mac):
    session = active_sessions.get(mac)

    if not session:
        return False

    if time.time() > session["expiry"]:
        session["active"] = False
        return False

    return True

def remove_session(mac):
    if mac in active_sessions:
        del active_sessions[mac]