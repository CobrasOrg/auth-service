from app.core.tokens import create_access_token
from app.schemas.user import UserType, OwnerOut, ClinicOut

def get_user_output_model(user: dict):
    user_copy = user.copy()
    user_copy.pop("password", None)

    if user_copy["userType"] == UserType.CLINIC:
        return ClinicOut(**user_copy)
    else:
        return OwnerOut(**user_copy)

def build_auth_response(user: dict) -> dict:
    token_data = {"sub": user["id"], "userType": user["userType"], "email": user["email"]}
    token = create_access_token(token_data)
    user_out = get_user_output_model(user)

    return {
        "success": True,
        "user": user_out,
        "token": token
    }

def build_base_response(success: bool = True, message: str = None) -> dict:
    response = {"success": success}
    if message:
        response["message"] = message
    return response
