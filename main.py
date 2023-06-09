from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from PIL import Image
from supabase import create_client, Client
from io import BytesIO
from config import PROJECT_URL, PUBLIC_API, DATABASE_PSWD

app = FastAPI()

class Event(BaseModel):
    name: str
    description: str
    start_day: str
    start_hour: str
    finish_day: str
    finish_hour: str
    preview_image: str
    event_image: str

@app.post("/create-event")
async def create_event(event: Event, preview_image: UploadFile = None, event_image: UploadFile = None):
    # Access the event properties
    event_name = event.name
    event_description = event.description
    start_day = event.start_day
    start_hour = event.start_hour
    finish_day = event.finish_day
    finish_hour = event.finish_hour
    preview_image = event.preview_image
    event_image = event.event_image

    # Save preview_image as PNG
    if preview_image is not None:
        image_data = await preview_image.read()
        image = Image.open(BytesIO(image_data))
        preview_image_path = f"preview_{event_name}.png"
        image.save(preview_image_path, "PNG")

    # Save event_image as PNG
    if event_image is not None:
        image_data = await event_image.read()
        image = Image.open(BytesIO(image_data))
        event_image_path = f"event_{event_name}.png"
        image.save(event_image_path, "PNG")

    return {"message": "Event created successfully"}

