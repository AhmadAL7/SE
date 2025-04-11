import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    # Explicitly set the templates folder path
    app = Flask(__name__, 
                template_folder=os.path.abspath('templates'),
                static_folder=os.path.abspath('static'))
    app.config.from_object(Config)

    db.init_app(app)
    from app.routes.reservations_routes import reservations_bp
    from app.routes.notifications_routes import notifications_bp
    from app.routes.manager_routes import manager_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.auth_routes import auth_bp
    
    
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    return app
