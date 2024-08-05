import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, Response, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, user_logged_in
import textbooks

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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

        if user and check_password_hash(user.password, password):
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

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    data = request.json
    user = current_user
    avatar = data['avatar']
    display_name = data['display-name']
    # school = data['school']
    year_level = data['year-level']

    user.avatar, user.display_name, user.year_level = avatar, display_name, year_level
    db.session.add(user)
    db.session.commit()

    return Response('Updated user', 200)


@app.route('/library')
def library():
    all_textbooks = Textbook.query.all()
    recent_textbook = request.cookies.get('recent-textbook')
    return render_template('library.html', avatar=current_user.avatar, all_textbooks=all_textbooks, recent_textbook=recent_textbook)

@app.route('/textbook/<string:book_code>/<int:book_id>')
def textbook_view(book_code, book_id):
    textbook = Textbook.query.filter_by(book_code=book_code, id=book_id).first()
    recent_textbook = f'{textbook.book_code}/{textbook.id}'
    build_data = textbooks.get_textbook_build_data(textbook.repository)
    resp = make_response(render_template('reader.html', avatar=current_user.avatar, textbook=textbook, build_data=build_data, recent_textbook=recent_textbook))
    resp.set_cookie('recent-textbook', recent_textbook)
    return resp

@app.route('/upload-centre')
@login_required
def upload_centre():
    if current_user.role == 'admin':
        pending_submissions = TextbookSubmission.query.all()
        return render_template('upload-centre.html', admin=True, pending=pending_submissions)
    return render_template('upload-centre.html', admin=False)

@app.route('/submit-textbook', methods=['POST'])
@login_required
def submit_textbook():
    repository = request.form.get('repository')
    metadata = textbooks.get_textbook_options(repository)['metadata']

    submission = TextbookSubmission(
        title=metadata['title'],
        repository=repository
    )
    db.session.add(submission)
    db.session.commit()

    return Response(f'Submission added: {submission.title}', 201)

@app.route('/delete-submission', methods=['POST'])
@login_required
def delete_submission():
    if current_user.role == 'admin':
        submission_id = request.json['submission-id']
        submission = TextbookSubmission.query.filter(TextbookSubmission.id == submission_id).first()
        db.session.delete(submission)
        db.session.commit()
        return Response(f'Deleted submission with id {submission_id}', 200)
    return Response('Unauthorized', 401)

@app.route('/approve-submission', methods=['POST'])
@login_required
def approve_submission():
    repository = request.json['repository']
    submission_id = request.json['submission-id']
    options = textbooks.get_textbook_options(repository)
    cover_colour = options['book']['cover']['colour']
    title = options['metadata']['title']
    book_code = textbooks.generate_book_code(title)

    authors = []
    for a in options['metadata']['authors']:
        q = Author.query.filter_by(name=a).all()
        if len(q) < 1:
            author = Author(name=a)
            db.session.add(author)
            db.session.commit()
        else:
            author = q[0]
        authors.append(author)

    pages = 20  # TODO: Count pages. Probably update metadata in OTE
    pdf = 'placeholder'  # TODO: Gen PDFs
    html = textbooks.get_textbook_html_url(repository)

    textbook = Textbook(title=title, repository=repository, book_code=book_code, pages=pages, pdf=pdf, html=html, authors=authors) if cover_colour is 'default' else Textbook(title=title, repository=repository, book_code=book_code, pages=pages, pdf=pdf, html=html, authors=authors, cover_colour=cover_colour)
    db.session.add(textbook)
    submission = TextbookSubmission.query.filter_by(id=submission_id).first()
    db.session.delete(submission)
    db.session.commit()

    return Response(f'Created textbook: {book_code}', 201)
