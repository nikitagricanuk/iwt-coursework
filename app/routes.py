from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, make_response, session
import os.path
from app.api.requests import login as backend_login
from app.api.requests import register as backend_register

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def global_context():
    nav = [
        { "title": "Home", "url": "/" },
        { "title": "Users", "url": "/users" },
        { "title": "Secrets (Shhh!!)", "url": "/secrets" },
        { "title": "About", "url": "/about" },
    ]
    return {
        "nav": nav
    }
    
@main.context_processor
def session_context():
    return {
        'logged_in': session.get('token') is not None,
        'username': session.get('username'),
        'token': session.get('token')
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

@main.route('/about')
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
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html', name="Login")


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
            return redirect(url_for('main.home'))
        else:
            flash('Something went wrong', 'danger')
    
    return render_template('register.html', name="Sign Up")

@main.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('main.home'))

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
