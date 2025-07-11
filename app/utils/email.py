def send_password_reset_email(to_email: str, token: str) -> bool:
    print(f"EMAIL sent to USER: {to_email} with TOKEN: {token}")