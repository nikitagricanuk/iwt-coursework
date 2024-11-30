import datetime
from flask import Flask
from .extensions import init_extensions
from .routes import main as main_blueprint
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    
    init_extensions(app)
    
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