import requests as r
from config import BASE_URL

base_url = BASE_URL


def post_call(endpoint: str, body: dict, header: dict, base_url: str) -> dict:
    url = base_url + endpoint
    response = r.post(url, json=body, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        raise TypeError


def get_call(endpoint: str, header: dict, base_url: str) -> dict:
    url = base_url + endpoint
    response = r.get(url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        raise TypeError


def get_call_params(endpoint: str, params, base_url: str, header: dict):
    url = base_url + endpoint
    params = params
    response = r.get(url, params=params, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()
