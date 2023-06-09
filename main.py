from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from loguru import logger as LOG

import requests as r

from upload_on_ipfs import upload_file_on_ipfs
from supabase_connection import insert_db

app = FastAPI()

class Event(BaseModel):
    name: str
    description: str
    start_day: str
    finish_day: str
    event_image: str
    preview_image: str



@app.post("/create_event")
async def create_event(event: Event):
    LOG.info(f'{insert_db(event_info=event.dict())}')
    return {"git":"good"}


@app.post("/upload_event_image")
def create_picture(first_art: UploadFile = File(...)):
    """Takes image file, returns url to IPFS Storage"""
    LOG.info(f"New NFT was initiated")
    ipfs_url = upload_file_on_ipfs(first_art.file)
    LOG.info(f"IPFS NTF url: {ipfs_url}")
    return {"event_image": ipfs_url}

@app.post("/upload_preview_image")
def create_picture(second_art: UploadFile = File(...)):
    """Takes image file, returns url to IPFS Storage"""

    LOG.info(f"New NFT was initiated")
    ipfs_url = upload_file_on_ipfs(second_art.file)
    LOG.info(f"IPFS NTF url: {ipfs_url}")
    return {"preview_image": ipfs_url}
