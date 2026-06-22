def validate_login(phone):
    if not phone or len(phone) < 10:
        return False
    return True