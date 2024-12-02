from functools import wraps
from flask_caching import Cache
from flask_compress import Compress
from config import REDIS_HOST, REDIS_PORT, USE_REDIS

cache = Cache()
compress = Compress()

def init_extensions(app):
    if USE_REDIS:
        # Cache configuration
        app.config['CACHE_TYPE'] = 'redis'
        app.config['CACHE_REDIS_HOST'] = REDIS_HOST
        app.config['CACHE_REDIS_PORT'] = REDIS_PORT
        app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    else:
        app.config['CACHE_TYPE'] = 'NullCache'
    
    cache.init_app(app)
    
    compress.init_app(app)
