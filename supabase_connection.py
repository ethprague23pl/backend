from supabase import create_client, Client
from config import PROJECT_URL, PUBLIC_API

def insert_db(event_info:dict):
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)  
    supabase.table("events").insert(event_info).execute()
    return {'Msg':'Created good'}