import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/log-in")
def log_in():
    return render_template('log-in.html')


@app.route("/sign-up")
def sign_up():
    return render_template('sign-up.html')

@app.route("/profile")
def profile():
    return render_template('profile.html', user_name='William Herring', year_level=11)
