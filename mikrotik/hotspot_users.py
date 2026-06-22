from mikrotik.client import get_mikrotik_api


def create_hotspot_user(username, password, profile):
    """
    Create MikroTik hotspot user
    """

    try:
        api = get_mikrotik_api()

        hotspot_users = api.get_resource("/ip/hotspot/user")

        hotspot_users.add(
            name=username,
            password=password,
            profile=profile
        )

        return {
            "status": "success",
            "message": f"User {username} created"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ----------------------------------------
# COMPATIBILITY ALIAS
# ----------------------------------------
def create_user(username, password, profile):
    """
    Backward-compatible wrapper
    """

    return create_hotspot_user(
        username,
        password,
        profile
    )


def disable_hotspot_user(username):
    """
    Disable hotspot user
    """

    try:
        api = get_mikrotik_api()

        hotspot_users = api.get_resource("/ip/hotspot/user")

        users = hotspot_users.get(name=username)

        for user in users:
            hotspot_users.set(
                id=user[".id"],
                disabled="yes"
            )

        return True

    except Exception:
        return False