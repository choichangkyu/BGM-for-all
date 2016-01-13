from flask_sqlalchemy import SQLAlchemy
from flask import Flask


from test import app
db = SQLAlchemy(app)

admin = Admin(app)