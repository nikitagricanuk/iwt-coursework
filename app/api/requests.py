import requests
from config import BACKEND_URL

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
        
        return response.json() if response.status_code == 200 else None
    
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
