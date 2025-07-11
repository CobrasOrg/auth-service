import re

def validate_current_password_exists(value: str):
    if not value:
        raise ValueError("Current password is required.")
    return value

def validate_password_data(value: str):
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one number.")
    return value

def validate_confirm_password(value: str, confirm: str):
    if value and value != confirm:
        raise ValueError("Passwords do not match.")
    return value

def validate_name_data(value: str):
    if not value or len(value.strip()) < 2:
        raise ValueError("Name must be at least 2 characters long.")
    return value.strip()

def validate_phone_data(value: str):
    digits = re.sub(r"\D", "", value)
    if len(digits) < 10:
        raise ValueError("Phone number should be at least 10 digits long.")
    return digits

def validate_address_data(value: str):
    if len(value.strip()) < 5:
        raise ValueError("Address must be at least 5 characters long.")
    return value.strip()

def validate_locality_data(value: str):
    if not value or len(value.strip()) < 2:
        raise ValueError("Locality is required.")
    return value.strip()

def validate_email_data(value: str):
    return value.strip().lower()

def validate_token_data(value: str):
    if not value or len(value.strip()) < 2:
        raise ValueError("Token is required.")
    return value.strip()