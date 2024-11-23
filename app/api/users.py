from app.api.requests import send_post_request
from config import BACKEND_PASSWORD, BACKEND_USERNAME

async def login(username: str, password: str):
    payload = f"username={username}&password={password}"
    
    response = await send_post_request("v1/auth/token/create", payload, False, "x-www-form-urlencoded")
    if response is not None:
        return response["session_id"] # return token

async def register(username: str, email: str, password: str):
    # Request primary token using the system account
    token = await login(BACKEND_USERNAME, BACKEND_PASSWORD)
    
    payload = {
        "username": username,
        "email": email,
        # since our backend doesn't support ACL yet, it's doesn't matter which role is used
        "roles": ["user"], 
        "password": password
    }
    return await send_post_request("v1/auth/users/create", payload, True, "json", token)

async def renew_token(token: str):
    """
    Renew the token.

    Args:
        token (str): The token to renew

    Returns:
        dict: A JSON from a server containing the renewed token information
        NoneType: If the token is invalid
    """
    return await send_post_request("v1/auth/token/renew", None, False, "json", token)
