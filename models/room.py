from db import db

class Room(db.Model):
    __tablename__ = "room"

    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True )
    person_sum = db.Column(db.Integer,default=10)
