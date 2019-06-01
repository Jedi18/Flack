from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    personal = db.Column(db.Boolean, default=False)
    messages = db.relationship("Message", backref="Channel", lazy=True)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    channel = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    sentby = db.Column(db.String, nullable=False, default="user")
    senton = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    channels = db.relationship("Channel", backref="Message", lazy=True)
