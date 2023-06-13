from supabase import create_client, Client
import json
from config import PROJECT_URL, PUBLIC_API
from user_security import hashpassword, generate_jwt_token, encode_jwt_token
from pydantic import BaseModel


class LoginResponse(BaseModel):
    accessToken: str


def insert_db(event_info: dict):
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)
    supabase.table("events").insert(event_info).execute()
    return {"Msg": "Created good"}


def create_user(user: dict):
    try:
        url: str = PROJECT_URL
        key: str = PUBLIC_API
        supabase: Client = create_client(url, key)
        generate_jwt_token(user["user_email"])
        user["user_password"] = hashpassword(user["user_password"])
        supabase.table("user_management").insert(user).execute()
        return {"accessToken": f"{generate_jwt_token(user['user_email'])}"}
    except ValueError:
        return ValueError


def fetch_user(user_email: str):
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)

    response = (
        supabase.table("user_management")
        .select("*")
        .eq("user_email", f"{user_email}")
        .execute()
    )
    return response


def get_private_key(jwt_token: str) -> str:
    for data in fetch_user(user_email=encode_jwt_token(jwt_token=jwt_token)):
        if type(data[1]) == list:
            return data[1][0]["wallet_private_key"]


def log_in(user_email: str, user_password: str) -> LoginResponse:
    for data in fetch_user(user_email=user_email):
        if type(data[1]) == list:
            if data[1][0]["user_password"] == None:
                continue
            elif data[1][0]["user_password"] == hashpassword(user_password):
                return {"accessToken": f"{generate_jwt_token(user_email)}"}
            else:
                raise TypeError()


def get_events():
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)

    response = supabase.table("events").select("*").execute()
    return response.data


# 0x18d39edD4F8b82C2fa630783c70c688ec4D83839
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hdGlAZ21haWwuY29tIiwiZXhwIjoxNzE4MjI4ODM2fQ.t6X1tNW1SA995rk2IRDqNQCr-Tie8T5Dy7uzgQ-u8xI
