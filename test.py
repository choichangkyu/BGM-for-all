from datetime import datetime

from flask import Flask, jsonify, render_template, request, make_response, session, redirect, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'asldjalksjdklasd'
admin = Admin(app)
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "user"
    idx = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, default=20)
    name = db.Column(db.String(20))
    id = db.Column(db.String(20), unique=True)
    pw = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.now)

class Comment(db.Model):
    __tablename__ = "comment"
    idx = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    who = db.Column(db.Integer, db.ForeignKey('user.idx'))

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

@app.route("/")
def index():

    return render_template('index.html')

#################################### Login
@app.route("/loginpage")
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['id']
    password = request.form['password']

    found = User.query.filter(
        User.id == username,
        User.pw == password,
    ).first()
    if found:
        session['logged_in'] = True
        resp = make_response(redirect(url_for("index"))  )
        resp.set_cookie('username', username)
        print(session['logged_in'])
        return resp
    else :
        return "Login Failed"
##################################### Sign

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')

@app.route("/signpage")
def sign_page():
    return render_template('sign.html')

@app.route("/sign" ,  methods=['GET', 'POST'])
def sign():
    new = User()
    new.name = request.form['nickname']
    new.id = request.form['id']
    new.pw = request.form['password']

    if not len(new.name) or not len(new.id) or not len(new.pw) :
        return "fuck"
    if is_already_registered(new.id, new.pw, new.name ) == 2:
        return "id"
    if is_already_registered(new.id, new.pw, new.name)== 3:
        return "pw"
    if is_already_registered(new.id, new.pw, new.name) == 4:
        return "name"
    db.session.add(new)
    db.session.commit()

    return render_template("login.html")

def is_already_registered(id,pw, name):
    found = User.query.filter(
        User.id == id,
    ).first()
    found2 = User.query.filter(
        User.pw == pw,
    ).first()
    found3 = User.query.filter(
        User.name == name,
    ).first()

    if found:
        return 2
    if found2:
        return 3
    if found3:
        return 4
    return False

@app.route("/success")
def success():
    username = request.cookies.get('username')
    return "<h1>" + str(username)
"""
@app.route("/search/<name>/<id>/<pw>")
def search(name, id, pw, is_web=True):
    found = User.query.filter(
        User.name == name,
        User.id == id,
        User.pw == pw,
    ).first()
    if found:
        if is_web:
            return 'success! %s' % (found.id, )
    else:
        return found

    if is_web:
        return 'failed'
    else:
        return None
"""
"""
@app.route("/delete/<name>/<id>/<pw>")
def delete(name, id, pw):
    found = search(name, id, pw, is_web=False)
    db.session.delete(found)
    db.session.commit()

    return 'deleted!'
"""
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)