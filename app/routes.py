from flask import Blueprint, render_template, send_from_directory
import os.path

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def global_context():
    nav = [
        { "title": "Главная", "url": "/" },
        { "title": "Архитектура", "url": "/arch" },
        { "title": "Секреты", "url": "/secrets" },
        { "title": "Пользователи", "url": "/users" },
    ]
    return {
        "nav": nav
    }

# Define a route inside the blueprint
@main.route('/')
async def home():
    return render_template('index.html', name="Главная")

@main.route('/secrets')
async def secrets():
    return render_template('secrets.html', name="Секреты")

@main.route('/users')
async def users():
    return render_template('users.html', name="Пользователи")

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
