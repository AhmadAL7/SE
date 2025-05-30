import os

class Config:
    # SQLite database URI
    SECRET_KEY = os.urandom(32).hex() # Secret key for session security
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'restaurant.db')}" # Specify the location of the db - current working dir 
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Reduce memory usage