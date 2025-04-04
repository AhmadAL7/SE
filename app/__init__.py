import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    # Explicitly set the templates folder path
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
