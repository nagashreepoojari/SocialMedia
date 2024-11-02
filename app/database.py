from flask import Flask
from .models import db

app = Flask(__name__)

DATABASE_URI = 'postgresql+psycopg2://postgres:Nagashree%40postgres@localhost:5432/flaskapi'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


