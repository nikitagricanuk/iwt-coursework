from functools import wraps

from flask import flash, redirect, session, url_for

from app.api.users import renew_token


def check_session(func):
    """
    Check if the session is valid.
    
    This decorator checks if the user's session token is valid 
    by calling the `check_token` function.
    If the token is invalid or expired, it flashes an error message 
    and redirects the user to the login page, otherwise renews it.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(session["token"])
        status = await renew_token(session["token"])
        print(status)
        if status is None:
            flash('Your session has expired, please log in again', 'danger')
            return redirect(url_for('main.login'))
        
        return await func(*args, **kwargs)
    
    return wrapper
