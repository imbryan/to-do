from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    todos = db.relationship('ToDO', backref='user', lazy=True)  # each user has multiple To-DOs


class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150), nullable=False)  # the text content of a To-DO
    due_date = db.Column(db.Date)  # a user set due date for a To-DO
    complete = db.Column(db.Boolean, nullable=False, default=False)  # completed flag for a To-DO

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # each To-DO associates with a user

