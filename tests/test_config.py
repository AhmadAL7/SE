import os

class TestConfig:
    TESTING = True
    SECRET_KEY = 'test'  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use temporary in-memory DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal tracking for performance
    WTF_CSRF_ENABLED = False  # Disable CSRF protection to simplify form testing

