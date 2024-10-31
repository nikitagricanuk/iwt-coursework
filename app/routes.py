from flask import Blueprint, render_template

# Create a blueprint
main = Blueprint('main', __name__)

# Define a route inside the blueprint
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')