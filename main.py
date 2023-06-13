from fastapi import FastAPI, UploadFile, File, Header, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from loguru import logger as LOG
from typing import List, Annotated
from upload_on_ipfs import upload_file_on_ipfs
from supabase_connection import (
    insert_db,
    create_user,
    log_in,
    LoginResponse,
    get_events,
    get_private_key,
)
from node_connection import post_call, get_call, get_call_params
from config import BASE_URL, header_function
from fastapi.middleware.cors import CORSMiddleware


class Event(BaseModel):
    name: str
    description: str
    start_day: str
    finish_day: str
    event_image: str
    preview_image: str
    contract_address: str
    ticket_quantity: int
    ticket_price: int


class User(BaseModel):
    user_email: str
    user_name: str
    user_password: str
    wallet_address: str
    wallet_private_key: str


class BuyTicket(BaseModel):
    ticketQuantity: int
    eventContractAddress: str
    privateKey: str


class Ticket(BaseModel):
    eventContractAddress: str
    walletPrivateKey: str


class Sell(BaseModel):
    eventContractAddress: str
    tokenId: int
    tokenPrice: float


class Buy(BaseModel):
    eventContractAddress: str
    tokenId: int


class Marketplace(BaseModel):
    jwt_token: str
    eventContractAddress: str
    tokenId: int


base_url = BASE_URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBasic()

# POST


@app.post("/marketplace/buy")
async def buy_ticket(buy: Buy, user_jwt: Annotated[str | None, Header()] = None):
    buy_body = {
        "privateKey": get_private_key(user_jwt),
        "eventContractAddress": buy.eventContractAddress,
        "tokenId": buy.tokenId,
    }
    return post_call(
        endpoint="/marketplace/buy",
        body=buy_body,
        header=header_function,
        base_url=base_url,
    )


@app.post("/marketplace/sell")
async def sell_ticket(sell: Sell, user_jwt: Annotated[str | None, Header()] = None):
    sell_body = {
        "privateKey": get_private_key(user_jwt),
        "eventContractAddress": sell.eventContractAddress,
        "tokenId": sell.tokenId,
        "tokenPrice": sell.tokenPrice,
    }
    return post_call(
        endpoint="/marketplace/sell",
        body=sell_body,
        header=header_function(user_jwt),
        base_url=base_url,
    )


@app.post("/ticket")
async def buy_ticket(
    ticket: BuyTicket, user_jwt: Annotated[str | None, Header()] = None
):
    ticket_body = {
        "ticketQuantity": ticket.ticketQuantity,
        "eventContractAddress": ticket.eventContractAddress,
        "privateKey": get_private_key(ticket.user_jwt),
    }
    return post_call(
        endpoint="/ticket", body=ticket_body, header=header_function, base_url=base_url
    )


@app.post("/event", response_model=dict)
async def create_event(event: Event):
    event.contract_address = next(
        iter(
            post_call(
                endpoint="/event",
                body={
                    "ticketQuantity": event.ticket_quantity,
                    "ticketPrice": event.ticket_price,
                },
                header=header_function,
                base_url=base_url,
            ).values()
        )
    )
    insert_db(event_info=event.dict())
    return {"addres": event.contract_address}


@app.post("/image", response_model=str)
async def create_picture(second_art: UploadFile = File(...)):
    """Takes image file, returns url to IPFS Storage"""
    ipfs_url = upload_file_on_ipfs(second_art.file)
    return ipfs_url


@app.post("/account", response_model=LoginResponse)
async def crete_account(user: User):
    user.wallet_address, user.wallet_private_key = get_call(
        endpoint="/account", header=header_function, base_url=BASE_URL
    ).values()
    return create_user(user=user.dict())


@app.post("/login", response_model=LoginResponse)
async def log_to_account(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return log_in(user_email=credentials.username, user_password=credentials.password)


# GET
@app.get("/list-tickets")
def get_list_tickets(
    eventContractAddress: str, user_jwt: Annotated[str | None, Header()] = None
):
    get_params = get_call_params(
        "/list-tickets",
        params={
            "eventContractAddress": eventContractAddress,
        },
        header=header_function(token=user_jwt),
        base_url=base_url,
    )
    return get_params


@app.get("/marketplace")
def get_marketplace(
    eventContractAddress: str,
    tokenId: int,
    user_jwt: Annotated[str | None, Header()] = None,
):
    get_params = get_call_params(
        "/marketplace",
        params={
            "privateKey": get_private_key(jwt_token=user_jwt),
            "eventContractAddress": eventContractAddress,
            "tokenId": tokenId,
        },
        base_url=base_url,
    )
    return get_params


@app.get("/ticket")
def get_ticket(
    eventContractAddress: str, user_jwt: Annotated[str | None, Header()] = None
):
    get_params = get_call_params(
        "/ticket",
        params={
            "eventContractAddress": eventContractAddress,
            "walletPrivateKey": get_private_key(jwt_token=user_jwt),
        },
        base_url=base_url,
    )
    return get_params


@app.get("/event", response_model=List[Event])
def get_event():
    return get_events()


@app.get("/")
def root():
    return {"working": "hard"}


@app.get("/users/")
async def get_user(user_jwt: Annotated[str | None, Header()] = None):
    return {"user_jwt": user_jwt}
