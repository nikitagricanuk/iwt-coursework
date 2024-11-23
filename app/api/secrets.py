from json import loads

from app.api.requests import send_get_request, send_post_request
from config import BACKEND_URL


async def create_secret(name: str, data, description: str, token: str, ttl: int = 0):
    payload = {
        "name": name,
        "data": {
            data
        },
        "tags": ["general"],
        "ttl": ttl,
        "description": description
    }

    response =  await send_post_request("v1/secrets/create", payload, True, "json", token)
    
    return loads(response) if response else None

async def list_all_secrets(token: str):
    return await send_get_request("v1/secrets", token)
