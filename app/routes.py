from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, make_response, session
import os.path
from app.api.users import login as backend_login
from app.api.users import register as backend_register
from app.api.secrets import create_secret, list_all_secrets
from app.api.decorators import check_session

# Create a blueprint
main = Blueprint('main', __name__)

@main.context_processor
def global_context():
    nav = [
        { "title": "Home", "url": "/" },
        { "title": "Users", "url": "/users" },
        { "title": "Secrets (Shhh!!)", "url": "/secrets" },
        { "title": "Glossary", "url": "/glossary" },
        { "title": "About", "url": "/about" },
    ]
    pages = [
        { "title": "Home", "url": "/" },
        { "title": "Users", "url": "/users" },
        { "title": "Secrets (Shhh!!)", "url": "/secrets" },
        { "title": "Glossary", "url": "/glossary" },
        { "title": "About", "url": "/about" },
        { "title": "Login", "url": "/login"},
        { "title": "Sign Up", "url": "/register"},
        
        { "title": "Home", "url": "/dashboard" },
        { "title": "Secrets", "url": "/dashboard/secrets"},
        { "title": "Users", "url": "/dashboard/users"},
        { "title": "Account", "url": "/dashboard/account"},
    ]
    return {
        "nav": nav,
        "pages": pages
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
    return render_template('index.html')

@main.route('/secrets')
async def secrets():
    return render_template('secrets.html')

@main.route('/users')
async def users():
    return render_template('users.html')

@main.route('/glossary')
async def glossary():
    return render_template('glossary.html')

@main.route('/about')
async def about():
    return render_template('about.html')

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
    return render_template('dashboard/home.html')

@main.route('/dashboard/secrets')
@check_session
async def dashboard_secrets():
    records = await list_all_secrets(session["token"])
    
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     form_data = request.form.get('data')
    #     description = request.form.get('password')
    #     ttl = request.form.get('ttl')
    #     token = session['token']
    #     response =  await create_secret(name, form_data, description, ttl,  token)
        
    #     if response is not None:
    #         session['username'] = username
    #         session['token'] = token
    #         return redirect(url_for('main.dashboard'))
    #     else:
    #         flash('Something went wrong', 'danger')
    return render_template('dashboard/secrets.html', records=records)

@main.route('/dashboard/users')
@check_session
async def dashboard_users():
    return render_template('dashboard/users.html')

@main.route('/dashboard/account')
@check_session
async def dashboard_account():
    return render_template('dashboard/account.html')

@main.route('/favicon.ico')
async def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/icons'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
