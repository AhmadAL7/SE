# create_db.py
from app import create_app, db
from app.models import *

# Create app
app = create_app()

# Create all tables 
with app.app_context():
    db.create_all()  # Creates all tables from your models
    print("Database tables created successfully!")