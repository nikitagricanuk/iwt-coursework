import requests
from config import BACKEND_URL, BACKEND_USERNAME, BACKEND_PASSWORD

async def login(username: str, password: str):
    payload = f"username={username}&password={password}"
    
    response = await send_post_request("v1/auth/token/create", payload, False, "x-www-form-urlencoded")
    if response is not None:
        return response["session_id"] # return token

async def register(username: str, email: str, password: str):
    # Request primary token using system account
    token = await login(BACKEND_USERNAME, BACKEND_PASSWORD)
    
    payload = {
        "username": username,
        "email": email,
        # since our backend doesn't support ACL yet, it's doesn't matter which role is used
        "roles": ["user"], 
        "password": password
    }
    return await send_post_request("v1/auth/users/create", payload, True, "json", token)

async def send_post_request(endpoint: str, payload, json: bool, content_type: str, token: str = None):
    url = f"{BACKEND_URL}/{endpoint}"
    headers = {
        "Content-Type": f"application/{content_type}",
        "Authorization": f"Bearer {token}" # we can pass None here, because if token is not needed, server just won't read it
    }
    
    try:
        if json:
            response = requests.post(url, json=payload, headers=headers)
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating request: {e}")
        return None

async def send_get_request(endpoint: str, token: str): 
    url = f"{BACKEND_URL}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating secret: {e}")
        return None
