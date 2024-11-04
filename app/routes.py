from flask import Blueprint, render_template, send_from_directory
import os.path

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def global_context():
    nav = [
        { "title": "Главная", "url": "/" },
        { "title": "Пользователи", "url": "/users" },
        { "title": "Секреты (ПССС!!)", "url": "/secrets" },
        { "title": "Об авторе", "url": "/about" },
    ]
    return {
        "nav": nav
    }

@main.route('/')
async def home():
    return render_template('index.html', name="Главная")

@main.route('/secrets')
async def secrets():
    return render_template('secrets.html', name="Секреты (ПССС!!)")

@main.route('/users')
async def users():
    return render_template('users.html', name="Пользователи")

@main.route('/about')
async def about():
    return render_template('about.html', name="Об авторе")

@main.route('/login')
async def login():
    return render_template('login.html', name="Вход")

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
