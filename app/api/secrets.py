from app.api.requests import send_get_request, send_post_request, send_delete_request
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
    
    return response or None

async def delete_secret(id: str, token: str):
    return await send_delete_request(f"v1/secrets/{id}", token)

async def list_all_secrets(token: str):
    return await send_get_request("v1/secrets", token)

async def get_secret(id: str, token: str):
    return await send_get_request(f"v1/secrets/{id}", token)
