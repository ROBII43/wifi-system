from routeros_api import RouterOsApiPool
from config import Config


def connect():
    pool = RouterOsApiPool(
        Config.MIKROTIK_HOST,
        username=Config.MIKROTIK_USER,
        password=Config.MIKROTIK_PASSWORD,
        plaintext_login=True
    )

    return pool.get_api()


# Alias for compatibility
get_mikrotik_api = connect