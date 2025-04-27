import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from sqlalchemy import Engine
from sqlalchemy import event 
# Use default config unless overridden by test
from app.config import Config

socketio = SocketIO(cors_allowed_origins="*")  #  restrict for production
db = SQLAlchemy()

#enforce foriegn key constraints
@event.listens_for(Engine, "connect")
def enforce_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    
def create_app(config_class=Config):  # Accept external config (for tests)
    app = Flask(__name__,
                template_folder=os.path.abspath('templates'),
                static_folder=os.path.abspath('static'))
    app.config.from_object(config_class)  # Use passed config

    socketio.init_app(app)
    db.init_app(app)

    # Import and register blueprints
    from app.routes.reservations_routes import reservations_bp
    from app.routes.notifications_routes import notifications_bp
    from app.routes.manager_routes import manager_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp

    app.register_blueprint(payment_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(manager_bp, url_prefix="/manager")
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(order_bp)

    return app
