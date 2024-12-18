import ast
from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, make_response, session
import os.path

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def pages_context():
    nav = [
        { "title": "Главная", "url": "/" },
        { "title": "Архитектура", "url": "/arch" },
        { "title": "Пользователи", "url": "/users" },
        { "title": "Секреты (Тсс!!)", "url": "/secrets" },
        { "title": "Глоссарий", "url": "/glossary" },
        { "title": "Обо мне", "url": "/about" }
    ]
    return {
        "nav": nav,
    }

@main.route('/')
async def home():
    return render_template('index.html', name="Главная")

@main.route('/arch')
async def arch():
    return render_template('arch.html', name="Архитектура")

@main.route('/secrets')
async def secrets():
    return render_template('secrets.html', name="Секреты (Тсс!!)")

@main.route('/users')
async def users():
    return render_template('users.html', name="Пользователи")

@main.route('/glossary')
async def glossary():
    return render_template('glossary.html', name="Глоссарий")

@main.route('/about')
async def about():
    return render_template('about.html', name="Обо мне")

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
