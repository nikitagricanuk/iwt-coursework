import datetime
from flask import Flask
from flask_caching import Cache
from flask_compress import Compress
from .routes import main as main_blueprint
from config import REDIS_HOST, REDIS_PORT, SECRET_KEY

cache = Cache()

def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    
    # Configure Flask-Caching with Redis
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = REDIS_HOST
    app.config['CACHE_REDIS_PORT'] = REDIS_PORT
    
    cache.init_app(app)

    Compress(app)
    
    # Convert time from timestamp to DD:MM:YY HH:SS
    @app.template_filter('format_datetime')
    def format_datetime(value):
        try:
            if value:
                dt = datetime.datetime.fromtimestamp(int(value))
                return dt.strftime('%d.%m.%Y %H:%M')
        except (ValueError, TypeError):
            return ''
        return ''
    
    app.register_blueprint(main_blueprint)

    return app