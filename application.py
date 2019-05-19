import os

from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        return render_template('index.html', channels=[], username=session['username'])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
