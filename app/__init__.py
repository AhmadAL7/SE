import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*") #I need to rsetrict this later
db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__, 
                template_folder=os.path.abspath('templates'),
                static_folder=os.path.abspath('static'))
    app.config.from_object(Config)
    socketio.init_app(app)   
    db.init_app(app) # link the db 
    from app.routes.reservations_routes import reservations_bp
    from app.routes.notifications_routes import notifications_bp
    from app.routes.manager_routes import manager_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.order_routes import order_bp
      
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(order_bp)
    return app
