from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from loguru import logger as LOG
from typing import List
from upload_on_ipfs import upload_file_on_ipfs
from supabase_connection import insert_db, create_user, log_in, LoginResponse, get_events, get_private_key
from node_connection import post_call, get_call, get_call_params
from config import BASE_URL
from requests import Response

from starlette.middleware.cors import CORSMiddleware


base_url = BASE_URL

header={'Content-Type': 'application/json'}

app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    # "http://localhost:3000"
    # "*",
    # "http://localhost:19000",
    # "ticketex2-production.up.railway.app",
    'https://front-brown-one.vercel.app/'
    # "https://ticketex2-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Event(BaseModel):
    name: str
    description: str
    start_day: str
    finish_day: str
    event_image: str
    preview_image: str
    contract_address: str
    ticket_quantity:int
    ticket_price: int
    # TODO
    # fix ticket_price more than 0 

class User(BaseModel):
    user_email: str
    user_name: str
    user_password: str
    wallet_address: str
    wallet_private_key: str 

class BuyTicket(BaseModel):
    jwt_token: str
    ticketQuantity: int
    eventContractAddress: str
    privateKey: str

class Ticket(BaseModel):
    eventContractAddress: str
    walletPrivateKey: str

# POST

@app.post('/ticket')
async def buy_ticket(ticket: BuyTicket):
    ticket_body={
    "ticketQuantity": ticket.ticketQuantity,
    "eventContractAddress": ticket.eventContractAddress,
    "privateKey": get_private_key(ticket.jwt_token)
    }
    return post_call(endpoint='/ticket', body = ticket_body,header={'Content-Type': 'application/json'}, base_url=base_url) 

@app.post("/event", response_model=dict)
async def create_event(event: Event):
    event.contract_address = next(iter(post_call(endpoint='/event', body={"ticketQuantity": event.ticket_quantity, "ticketPrice":event.ticket_price}, header={'Content-Type': 'application/json'}, base_url=base_url).values()))
    insert_db(event_info=event.dict())
    return {"addres":event.contract_address}

@app.post("/image", response_model=str)
def create_picture(second_art: UploadFile = File(...)):
    """Takes image file, returns url to IPFS Storage"""
    ipfs_url = upload_file_on_ipfs(second_art.file)
    return ipfs_url

@app.post("/account", response_model=LoginResponse)
def crete_account(user: User):    
    user.wallet_address, user.wallet_private_key = get_call(endpoint="/account", header={'Content-Type': 'application/json'}, base_url=BASE_URL).values()
    return create_user(user = user.dict())
    

@app.post("/login", response_model=LoginResponse)
def log_to_account(user_email:str, user_password:str):
    return log_in(user_email=user_email, user_password=user_password)


# GET
@app.get('/ticket')
def get_ticket(eventContractAddress:str, jwt_token:str):
    get_params = get_call_params('/ticket',params={
    "eventContractAddress": eventContractAddress,
    "walletPrivateKey": get_private_key(jwt_token=jwt_token)
}, base_url=base_url)
    return get_params

@app.get("/event", response_model=List[Event])
def get_event():
    return get_events()

@app.get("/")
def root():
    return {'working':'hard'}

ALLOWED_ORIGINS = '*'

# @app.middleware("https")
# async def add_CORS_header(request, call_next):
#     response = await call_next(request)
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response

# # handle CORS preflight requests
# @app.options('/{rest_of_path:path}')
# async def preflight_handler(request, rest_of_path):
#     response = Response()
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response