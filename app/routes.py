import ast
from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, make_response, session
import os.path

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def pages_context():
    nav = [
        { "title": "Home", "url": "/" },
        { "title": "Users", "url": "/users" },
        { "title": "Secrets (Shhh!!)", "url": "/secrets" },
        { "title": "Glossary", "url": "/glossary" },
        { "title": "About", "url": "/about" },
    ]
    return {
        "nav": nav,
    }

@main.route('/')
async def home():
    return render_template('index.html', name="Home")

@main.route('/secrets')
async def secrets():
    return render_template('secrets.html', name="Secrets (Shhh!!)")

@main.route('/users')
async def users():
    return render_template('users.html', name="Users")

@main.route('/glossary')
async def glossary():
    return render_template('glossary.html', name="Glossary")

@main.route('/about')
async def about():
    return render_template('about.html', name="About")

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
