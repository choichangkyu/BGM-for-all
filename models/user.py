from db import db
from datetime import datetime

class User(db.Model):

    __tablename__ = "user"
    idx = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, default=19)
    name = db.Column(db.String(30) )
    id = db.Column(db.String(10), unique=True)
    pw = db.Column(db.String(200))
    room = db.Column(db.String(20), default=None)
    created = db.Column(db.DateTime, default=datetime.now)
