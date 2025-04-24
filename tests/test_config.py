import os

class TestConfig:
    TESTING = True
    SECRET_KEY = 'test'  # Secure sessions in test context
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use temporary in-memory DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal tracking for performance
    WTF_CSRF_ENABLED = False  # Disable CSRF to simplify form testing

    # Optional: Future-proofing for uploads, mail, caching, etc.
    # UPLOAD_FOLDER = '/tmp/uploads'
    # MAIL_SUPPRESS_SEND = True
