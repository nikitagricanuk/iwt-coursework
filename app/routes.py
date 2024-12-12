import ast
from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, make_response, session
import os.path
from app.api.users import login as backend_login
from app.api.users import register as backend_register
from app.api.secrets import create_secret, list_all_secrets
from app.api.decorators import check_session
from config import BACKEND_URL
from .extensions import cache

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
    dash_nav = [
        { "title": "Home", "url": "/dashboard", "icon": "house"},
        { "title": "Secrets", "url": "/dashboard/secrets", "icon": "key"},
    ]
    return {
        "nav": nav,
        "dash_nav": dash_nav
    }
    
@main.context_processor
def session_context():
    return {
        'logged_in': session.get('token') is not None,
        'username': session.get('username'),
        'token': session.get('token')
    }

@main.context_processor
def backend_context():
    return {
        'backend_url': f"{BACKEND_URL}"
    }

@main.route('/')
@cache.cached(timeout=60)
async def home():
    return render_template('index.html', name="Home")

@main.route('/secrets')
@cache.cached(timeout=60)
async def secrets():
    return render_template('secrets.html', name="Secrets (Shhh!!)")

@main.route('/users')
@cache.cached(timeout=60)
async def users():
    return render_template('users.html', name="Users")

@main.route('/glossary')
@cache.cached(timeout=60)
async def glossary():
    return render_template('glossary.html', name="Glossary")

@main.route('/about')
@cache.cached(timeout=60)
async def about():
    return render_template('about.html', name="About")

@main.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST': # then we're receiving data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        token = await backend_login(username, password)
        
        if token is not None:  # Then everything is okay, proceed to set session data and redirect user to the home page
            session['username'] = username
            session['token'] = token
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        token =  await backend_register(username, email, password)
        
        if token is not None:
            session['username'] = username
            session['token'] = token
            return redirect(url_for('main.dashboard'))
        else:
            flash('Something went wrong', 'danger')
    
    return render_template('register.html')

@main.route('/logout')
async def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@check_session
async def dashboard():
    return render_template('dashboard/home.html', name="Home")

@main.route('/dashboard/secrets', methods=['GET', 'POST'])
@check_session
async def dashboard_secrets():
    token =  session['token']
    records = await list_all_secrets(token)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        data = request.form.get('data')
        
        response = await create_secret(name, data, description, token)
        
        if response is not None:
            flash('Secret created successfully. Please reload the page.', 'success')
        else:
            flash('Something went wrong', 'danger')
            
        # Redirect to avoid form resubmission on reload
        return redirect(url_for('main.dashboard_secrets'))
            
    return render_template('dashboard/secrets.html', records=records, name="Secrets")

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
