from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/log-in")
def log_in():
    return render_template('log-in.html')


@app.route("/sign-up")
def sign_up():
    return render_template('sign-up')
