from flask import Blueprint, render_template, send_from_directory
import os.path

# Create a blueprint
main = Blueprint('main', __name__)

# Define a route inside the blueprint
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/about')
def about():
    return render_template('about.html')