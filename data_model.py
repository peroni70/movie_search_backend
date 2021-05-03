from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////movie_search.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

class Movies(db.Model, SerializerMixin):
    index = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(120), unique=True, nullable=False)
    movie_title = db.Column(db.String(120), unique=True, nullable=False)
    movie_desc = db.Column(db.String(120), unique=True, nullable=False)
