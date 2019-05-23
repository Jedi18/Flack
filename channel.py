from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    channel = db.Column(db.String, db.ForeignKey("channels.id"), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    channels = db.relationship("Channel", backref="Message", lazy=True)
