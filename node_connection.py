import requests as r
from config import BASE_URL
from supabase_connection import get_private_key
base_url = BASE_URL

acconut_endpoint = "/account"
event_endpoint = "/event"
ticket_endpoint = "/ticket"


def post_call(endpoint:str, body:dict, header:dict, base_url: str) -> dict:
    url = base_url + endpoint
    response = r.post(url, json = body, headers=header)
    if response.status_code == 200:
        return(response.json())
    else:
        raise TypeError

def get_call(endpoint:str, header:dict, base_url: str) -> dict:
    url = base_url + endpoint
    response = r.get(url, headers=header)
    if response.status_code == 200:
        return(response.json())
    else:
        raise TypeError
    
def get_call_params(endpoint:str, params, base_url:str):
    url = base_url + endpoint
    params = params
    response = r.get(url, params=params)
    if response.status_code == 200:
        return (response.json())
    else:
        return {'fail':'big'}
    
header={
    'Content-Type': 'application/json'    
}

event = {
    "ticketQuantity": 100,
    "ticketPrice": 0
}



#print(get_call(endpoint=acconut_endpoint, header=header, base_url=base_url).values())
#print(next(iter(post_call(endpoint=event_endpoint, body=event, header=header, base_url=base_url).values())))
#print(asd)
# get_call(endpoint="/account", header={'Content-Type': 'application/json'}, base_url=BASE_URL)
#print(user)
#print(post_call(endpoint="/ticket", body=ticket_body, header=header, base_url=base_url))