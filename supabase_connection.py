from supabase import create_client, Client
from config import PROJECT_URL, PUBLIC_API

def insert_db(event_info:dict):
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)  
    supabase.table("events").insert(event_info).execute()
    return {'Msg':'Created good'}


def create_user(user:dict):
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)

    supabase.table("user_management").insert(user).execute()
    return {"User": "Added succesfully"}

def fetch_user():
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)
    
    response = supabase.table("user_management").select("*").execute()
    return response

def check_user(user_email:str, user_password: str):
    for userss in fetch_user():
        if type(userss[1]) == list:
            for data in userss[1]:
                if data['user_email'] == user_email and data['user_password'] == user_password:
                    return {'accesstoken':data["user_name"]}
    