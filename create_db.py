# create_db.py
from app import create_app, db
from app.models import * # import the models so db has access to them

app = create_app()
# Create all tables 
def create_database():
    with app.app_context():# actviates the app in temp envi so it can run functions
        db.create_all() # looks at all classes that inherit from db.model(*) & Creates all tables from  models
        print("Database created successfully with all tables.")

if __name__ == "__main__":
    create_database()
