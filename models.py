import random
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from app import db
from wonderwords import RandomWord

r = RandomWord()

# TODO: Many-to-many for users-books
textbooks_authors = db.Table(
    "textbooks_authors",
    db.Column("textbook_id", db.Integer, db.ForeignKey("textbook.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(200))
    year_level = db.Column(db.Integer)
    avatar = db.Column(db.String(500), default="https://hostedboringavatars.vercel.app/api/beam")
    role = db.Column(db.String(50), default="student")
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password, name=None):
        if name is None:
            self.display_name = r.word(include_parts_of_speech=['adjectives']) + r.word(include_parts_of_speech=['nouns']) + str(random.randint(1, 50))
        else:
            self.display_name = name

        self.avatar = f"https://hostedboringavatars.vercel.app/api/beam?name={self.display_name}"
        self.email = email
        self.password = generate_password_hash(password)
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<User {self.id}>"

class Textbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    book_code = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    cover_colour = db.Column(db.String(7), default="#db1a57")
    pages = db.Column(db.Integer, nullable=False)
    repository = db.Column(db.String(500), nullable=False)
    pdf = db.Column(db.String(500), nullable=False)
    html = db.Column(db.String(500), nullable=False)
    authors = db.relationship("Author", secondary=textbooks_authors, back_populates="textbooks")

    def __repr__(self):
        return f"<Textbook {self.book_code}>"

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    textbooks = db.relationship("Textbook", secondary=textbooks_authors, back_populates="authors")


class TextbookSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    repository = db.Column(db.String(500), nullable=False)
