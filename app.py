import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, Response, make_response, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, user_logged_in
import textbooks
import exports

# Configuration
load_dotenv()
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

from models import *

with app.app_context():
    db.create_all()  # Create tables
    db.session.commit()

@app.route("/")
def index():
    if session:
        return redirect('/library')
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()  # This isn't really used but a useful tool for admin

@app.route("/log-in", methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()  # Match the user with the email

        if user and check_password_hash(user.password, password):  # Check the password hash
            login_user(user)
            return redirect('/library')

    return render_template('log-in.html')

@app.route("/sign-up", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Create a user with credentials
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
    editing = request.args.get('editing') == '1'  # This stores the editing state
    return render_template('profile.html', editing=editing, user_name=current_user.display_name, avatar=current_user.avatar, year_level=current_user.year_level)

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    data = request.json
    user = current_user
    avatar = data['avatar']
    display_name = data['display-name']
    # There is no support for schools or classes in the app but the field exists, so it can possibly be implemented in the future
    # school = data['school']
    year_level = data['year-level']

    user.avatar, user.display_name, user.year_level = avatar, display_name, year_level
    db.session.add(user)
    db.session.commit()

    return Response('Updated user', 200)


@app.route('/library')
def library():
    all_textbooks = Textbook.query.all()
    recent_textbook = Textbook.query.filter_by(book_code=request.cookies.get('recent-textbook').split('/')[0]).first()  # The recent textbook is stored in a cookie
    return render_template('library.html', avatar=current_user.avatar, all_textbooks=all_textbooks, recent_textbook=recent_textbook)

@app.route('/textbook/<string:book_code>/<int:book_id>')
def textbook_view(book_code, book_id):
    textbook = Textbook.query.filter_by(book_code=book_code, id=book_id).first()
    recent_textbook = f'{textbook.book_code}/{textbook.id}'  # By storing a sliced version of the recent textbook's URL, it's easy to work with
    build_data = textbooks.get_textbook_build_data(textbook.repository)
    page_number = int(request.args.get('page')) if request.args.get('page') is not None else 0
    show_questions = request.args.get('mode') == 'questions'  # When switched to the questions tab, there is no page reload but the URL is modified to add the ?mode=questions argument so the tab selection will persist if there is a page reload
    resp = make_response(render_template('reader.html', avatar=current_user.avatar, textbook=textbook, build_data=build_data, page=page_number, show_questions=show_questions))
    resp.set_cookie('recent-textbook', recent_textbook)  # Set recent textbook
    return resp

@app.route('/upload-centre')
@login_required
def upload_centre():
    # Only admins can see pending submissions
    if current_user.role == 'admin':
        pending_submissions = TextbookSubmission.query.all()
        return render_template('upload-centre.html', admin=True, pending=pending_submissions)
    return render_template('upload-centre.html', admin=False)

@app.route('/submit-textbook', methods=['POST'])
@login_required
def submit_textbook():
    repository = request.form.get('repository')
    metadata = textbooks.get_textbook_options(repository)['metadata']

    # Textbook submissions are their own separate table because there is no need to compile and store an entire textbook if it is yet to be approved
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
    # This is an admin-only endpoint
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
    # Collect all basic metadata
    repository = request.json['repository']
    submission_id = request.json['submission-id']
    options = textbooks.get_textbook_options(repository)
    cover_colour = options['book']['cover']['colour']
    title = options['metadata']['title']
    book_code = textbooks.generate_book_code(title)
    # Generate a PDF
    pdf = exports.export_pdf(repository, book_code)

    # Cycle through authors and create an instance if one doesn't exist
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

    # Get HTML
    html = textbooks.get_textbook_html_url(repository)

    # Add to database
    textbook = Textbook(title=title, repository=repository, book_code=book_code, pdf=pdf, html=html, authors=authors) if cover_colour == 'default' else Textbook(title=title, repository=repository, book_code=book_code, pdf=pdf, html=html, authors=authors, cover_colour=cover_colour)
    db.session.add(textbook)
    submission = TextbookSubmission.query.filter_by(id=submission_id).first()
    db.session.delete(submission)
    db.session.commit()

    return Response(f'Created textbook: {book_code}', 201)

@app.route('/uploads/<name>')
def download_file(name):
    # This endpoint exists for file access
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)
