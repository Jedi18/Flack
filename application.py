import os

from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from channel import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:password@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        channels = Channel.query.all()
        return render_template('index.html', channels=channels, username=session['username'])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('index'))

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method=='GET':
        return render_template("create.html")
    else:
        channel_name = request.form.get('channel')

        chan = Channel(name = channel_name)
        db.session.add(chan)
        db.session.commit()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
