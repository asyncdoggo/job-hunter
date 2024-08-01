import firebase_admin
import firebase_admin.auth
from fastapi import Request


def get_current_user(request: Request):
    # fetch token from authorization header
    try:
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "No token provided"}
        token = token.split(" ")[1]
        decoded_token = firebase_admin.auth.verify_id_token(
            token, clock_skew_seconds=10)
        user = firebase_admin.auth.get_user(decoded_token["uid"])
        if user.email_verified:
            return decoded_token
        else:
            return {"error": "Email not verified"}
    except Exception as e:
        print(e)
        return {"error": "Invalid token"}
