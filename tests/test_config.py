import os

class TestConfig:
    TESTING = True # enabling flask tesing mode for better error display
    SECRET_KEY = 'test'   # for sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use temporary in-memory DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal tracking for performance


