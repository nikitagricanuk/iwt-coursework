import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')
BACKEND_USERNAME = os.getenv('BACKEND_USERNAME')
BACKEND_PASSWORD = os.getenv('BACKEND_PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')