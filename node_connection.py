import requests as r
from config import BASE_URL
from supabase_connection import get_private_key
base_url = BASE_URL

acconut_endpoint = "/account"
event_endpoint = "/event"
ticket_endpoint = "/ticket"


def post_call(endpoint:str, body:dict, header:dict, base_url: str):
    url = base_url + endpoint
    response = r.post(url, json = body, headers=header)
    return(response.json())
    # if response.status_code == 200:
    #     return(response.json())
    # else:
    #     raise TypeError
def post_call_ticket(endpoint:str, body:dict, header:dict, base_url: str):
    url = base_url + endpoint
    r.post(url, json = body, headers=header)
    

def get_call(endpoint:str, header:dict, base_url: str):
    url = base_url + endpoint
    response = r.get(url, headers=header)
    return(response.json())
    # if response.status_code == 200:
    #     return(response.json())
    # else:
    #     raise TypeError

header={
    'Content-Type': 'application/json'    
}

event = {
    "ticketQuantity": 100,
    "ticketPrice": 0
}

ticket_body={
  "ticketQuantity": 1,
  "eventContactAddress": "0x00324B1eb4D2fd83cc730cA82f54F9DC7dCd8611 ",
  "privateKey": get_private_key("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hdGkzM0BnbWFpbC5jb20iLCJleHAiOjE3MTc5Njk2NDV9.BG-evZkQ8wz94rfeRq7nf4ppytixf2Lrrr9OFMBXxyM")
}


#print(get_call(endpoint=acconut_endpoint, header=header, base_url=base_url).values())
#print(next(iter(post_call(endpoint=event_endpoint, body=event, header=header, base_url=base_url).values())))
#print(asd)
# get_call(endpoint="/account", header={'Content-Type': 'application/json'}, base_url=BASE_URL)
#print(user)
#print(post_call(endpoint="/ticket", body=ticket_body, header=header, base_url=base_url))