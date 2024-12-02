import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')
BACKEND_USERNAME = os.getenv('BACKEND_USERNAME')
BACKEND_PASSWORD = os.getenv('BACKEND_PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')

USE_REDIS = (os.getenv('USE_REDIS').lower() == 'true')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT')