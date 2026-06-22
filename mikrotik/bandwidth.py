from .client import connect

def set_speed(username, rate_limit):
    api = connect()
    users = api.get_resource("/ip/hotspot/user")

    user = users.get(name=username)

    if user:
        users.set(
            id=user[0]['id'],
            rate_limit=rate_limit
        )