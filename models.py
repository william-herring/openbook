from datetime import datetime
from app import bcrypt
from flask_login import UserMixin
from app import db

# TODO: Many-to-many for users-books and books-authors

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(200))
    avatar = db.Column(db.String(500), default="https://hostedboringavatars.vercel.app/api/beam")
    role = db.Column(db.String(50), default="student")
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password):
        self.email = email
        pwhash = bcrypt.generate_password_hash(password)
        self.password = pwhash.decode('utf8')
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<User {self.id}>"

class Textbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    book_code = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    repository = db.Column(db.String(500), nullable=False)
    pdf = db.Column(db.String(500), nullable=False)
    html = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Textbook {self.book_code}>"

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)