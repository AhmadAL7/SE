from app import create_app, db
app = create_app()
app.app_context().push()

# Drop all tables
db.drop_all()

# Recreate all tables from current models
db.create_all()
