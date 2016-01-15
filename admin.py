from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models.user import User
from models.room import Room


from db import db, Comment

admin = Admin()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Room, db.session))