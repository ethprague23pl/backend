from supabase import create_client, Client
import json
import io
import requests as r 

from PIL import Image
from config import PROJECT_URL, PUBLIC_API, DATABASE_PSWD, NFT_STORAGE_API
from loguru import logger as LOG

def db_client():
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)
    return supabase
