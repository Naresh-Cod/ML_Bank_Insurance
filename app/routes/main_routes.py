from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)  # _ Blueprint name = "main"

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/forms')
def forms():
    return render_template('forms.html')
