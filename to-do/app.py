from flask import Flask, redirect, url_for, render_template, request
from models import db
from decouple import config

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

# db.create_all()


@app.route("/")
def index():
    '''
    Home page
    '''
    return "Hello World"



if __name__ == "__main__":
    app.run(port=3000)
