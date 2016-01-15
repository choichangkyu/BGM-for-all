from flask_sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Comment(db.Model):
    __tablename__ = "comment"
    idx = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    who = db.Column(db.Integer, db.ForeignKey('user.idx'))
