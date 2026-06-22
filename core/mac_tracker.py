# Active device registry
device_registry = {}


def register_mac(mac, phone):
    """
    Register device MAC address
    """

    device_registry[mac] = {
        "phone": phone,
        "authorized": True
    }


def bind_mac_to_session(mac, phone):
    """
    Compatibility wrapper for ISP session binding
    """

    register_mac(mac, phone)

    return True


def is_mac_authorized(mac):
    """
    Check if device is authorized
    """

    return device_registry.get(mac, {}).get(
        "authorized",
        False
    )


def block_mac(mac):
    """
    Block device access
    """

    if mac in device_registry:
        device_registry[mac]["authorized"] = False


def remove_mac(mac):
    """
    Remove device from registry
    """

    if mac in device_registry:
        del device_registry[mac]