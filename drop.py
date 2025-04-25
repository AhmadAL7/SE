from app import create_app, db
app = create_app()
app.app_context().push()

# Drop all tables
db.drop_all()

db.metadata.clear()


