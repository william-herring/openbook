import os
from flask import Flask, render_template, request, redirect, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, user_logged_in

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

from models import *

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/")
def index():
    if session:
        return redirect('/library')
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@app.route("/log-in", methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/library')

    return render_template('log-in.html')

@app.route("/sign-up", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect('/profile?editing=1')

    return render_template('sign-up.html')

@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect('/log-in')

@app.route('/profile')
@login_required
def profile():
    editing = request.args.get('editing') == '1'
    return render_template('profile.html', editing=editing, user_name=current_user.display_name, avatar=current_user.avatar, year_level=current_user.year_level)

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/upload-centre')
@login_required
def upload_centre():
    admin = current_user.role == 'admin'
    return render_template('upload-centre.html', admin=admin)