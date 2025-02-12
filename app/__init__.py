from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # _ Load environment variables
    app = Flask(__name__)

    # _ Load API Key from .env
    app.config['API_KEY'] = os.getenv("API_KEY")

    if not app.config['API_KEY']:
        raise ValueError("⚠️ API_KEY is missing! Check your .env file.")

    # _ Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
