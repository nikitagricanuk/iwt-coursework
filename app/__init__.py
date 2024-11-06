from flask import Flask
from .routes import main as main_blueprint
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    
    app.register_blueprint(main_blueprint)

    return app