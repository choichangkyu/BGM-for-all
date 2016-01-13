from datetime import datetime
from  db import db

class User(db.Model):
    IDX = db.Column(db.String(20), primary_key = True )
    AGE = db.Column(db.Integer)
    NAME = db.Column(db.String(20), primary_key=True )
    ID = db.Column(db.String(50) , primary_key = True )
    PW = db.Column(db.String(50) )
    CREATED = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, id, pw, name, age):
        self.id = id
        self.pw = pw
        self.name = name
        self.age = age