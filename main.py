from supabase import client

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from supabase import create_client, Client
from loguru import logger as LOG
from datetime import datetime, time

import requests as r

from upload_on_ipfs import upload_file_on_ipfs
from config import PROJECT_URL, PUBLIC_API, DATABASE_PSWD



app = FastAPI()

class Event(BaseModel):
    LOG.info('cyce')
    name: str
    description: str
    start_day: datetime
    start_hour: time
    finish_day: datetime
    finish_hour: time

def update_db(event: Event, preview_image_url, event_image_url):
    LOG.info('dupa')
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)  

    supabase.table("events").insert({
  "name": event.name,
  "description": event.description,
  "start_day": event.start_day,
  "start_hour": event.start_hour,
  "finish_day": event.finish_day,
  "finish_hour": event.finish_hour,
  "preview_image": preview_image_url,
  "event_image": event_image_url}).execute()
    return {'Msg':'Created good'}


@app.post("/create_event")
async def create_event(event: Event):
    return {'Git':"Good"}

@app.post("/upload_image")
def create_picture(first_art: UploadFile = File(...)):
    """Takes image file, returns url to IPFS Storage"""

    LOG.info(f"New NFT was initiated")

    ipfs_url = upload_file_on_ipfs(first_art.file)

    LOG.info(f"IPFS NTF url: {ipfs_url}")

    return {"url": ipfs_url}
