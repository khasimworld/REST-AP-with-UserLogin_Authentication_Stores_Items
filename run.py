from app import app
from db import db

db.init_app(app)

#creates tables before the first request
@app.before_first_request 
def create_tables():
  db.create_all()