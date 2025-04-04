from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()  # Initialize SQLAlchemy

def create_app():
    app = Flask(__name__)   # Create the Flask application
    app.config.from_object(Config)  # Use the configuration file

    db.init_app(app)  # Bind SQLAlchemy to the app

    return app