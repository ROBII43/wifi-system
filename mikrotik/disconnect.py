from .client import connect

def disconnect_user(username):
    api = connect()
    active = api.get_resource("/ip/hotspot/active")

    sessions = active.get(user=username)

    for session in sessions:
        active.remove(id=session['id'])