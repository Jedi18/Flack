import os

from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

CHANNEL_MESSAGE_LIMIT = 100

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
        if session.get('lastchannel') is None:
            return redirect(url_for('channellist'))
        else:
            return redirect(url_for('channel', id=session['lastchannel']))

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

@app.route("/channel")
def channel():
    id = request.args.get("id")
    channel = Channel.query.get(id)
    messages = Message.query.filter_by(channel=id).order_by(desc(Message.senton)).limit(20).all()
    channel_send = {"name":channel.name.title(), "id":channel.id}
    messages_send = [{"message":message.message, "sentby":message.sentby, "senton":message.senton.strftime("%H:%M")} for message in messages]

    messages_send.reverse()

    session['lastchannel'] = id

    # remove if more than 100 messages
    message_tobedel = Message.query.filter_by(channel=id).order_by(desc(Message.senton)).offset(CHANNEL_MESSAGE_LIMIT).all()

    if message_tobedel:
        for message in message_tobedel:
            db.session.delete(message)
        db.session.commit()

    return render_template("channel.html", messages=messages_send, channel=channel_send)

@app.route("/channellist")
def channellist():
    channels = Channel.query.all()
    return render_template('index.html', channels=channels, username=session['username'])

@socketio.on("submit message")
def submitmessage(data):
    mess = data['message']
    channelid = data['channelid']
    message = Message(message=mess, channel=int(channelid), sentby=session['username'])
    senton = datetime.datetime.utcnow().strftime("%H:%M")
    db.session.add(message)
    db.session.commit()

    emit("message recieve", {"mess":mess, "sentby":session['username'], "senton":senton}, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
