import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, \
    render_template, request, make_response, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


from admin import admin
from db import db, migrate, Comment
from models.user import User
from models.room import Room


app = Flask(__name__)
app.config.from_pyfile("configs.py")

db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
socketio = SocketIO(app)

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
        session['username'] = username
        session['logged_in'] = True
        resp = make_response(redirect(url_for("wait")) )
        resp.set_cookie('username', username)
        print(session['logged_in'], session['username'])
        return resp, session['username']
    else :
        return "Login Failed"
##################################### Sign

@app.route("/logout")
def logout():

    session.pop(session['username'], None)
    session['logged_in'] = False
    return render_template('index.html')

@app.route("/signpage")
def sign_page():
    return render_template('sign.html')

@app.route("/sign" ,  methods=['GET', 'POST'])
def sign():
    new = User()
    new.id = request.form['id']
    new.pw = request.form['password']
    new.name = request.form['nickname']

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


@app.route("/wait")
def wait():

    return render_template('wait.html', room_lists = Room)


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
@socketio.on('my event', namespace='/test')
def test_message(message): # echo
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message): # broad
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socketio.on('want_room_lists', namespace='/test')
def get_room_lists():
    emit('send_room_lists',
         {'data': ', '.join(room_lists)}
    )

room_lists = []



@socketio.on('makeroom', namespace='/test')
@app.route('/makeroom' , methods=['GET', 'POST'])
def make_room(message):
    room_name = request.form['make_room']
    new_room = Room()
    new_room.name = room_name
    print("new room")
    if not len(new_room.name) :
        return "fuck"
    if is_already_room(new_room.name) == 1:
        return "있음"
    db.session.add(new_room)
    db.session.commit()
    join_room(message['room'])
    join_room(message['room'] + "_")
    if not message['room'] in room_lists:
        room_lists.append(message['room'])

    session['receive_count'] = session.get('receive_count', 0) + 1

    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'room': message['room'],
          'count': session['receive_count']},
         room=message['room'] )

    User.room = message['room']
    print(message['room'])
    return (render_template("room.html") , room_lists)
    """
    room_name = request.form['make_room']
    new_room = Room()
    new_room.name = room_name
    print("new room")
    if not len(new_room.name) :
        return "fuck"
    if is_already_room(new_room.name) == 1:
        return "있음"
    db.session.add(new_room)
    db.session.commit()
    join_room(room_name)
    join_room(room_name + "_")
    if not new_room.name in room_lists:
        room_lists.append(room_name)
    session['receive_count'] = session.get('receive_count', 0) + 1

    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'room': room_name,
          'count': session['receive_count']},
         room=room_name )

    return render_template("room.html")
    """

def is_already_room(name):
    found = Room.query.filter(
        Room.name == name,
    ).first()
    if found:
        return 1
    return False



@socketio.on('join', namespace='/test')
def join(message):          # join

    join_room(message['room'])
    join_room(message['room'] + "_")
    if not message['room'] in room_lists:
        room_lists.append(message['room'])

    session['receive_count'] = session.get('receive_count', 0) + 1

    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'room': message['room'],
          'count': session['receive_count']},
         room=message['room'] )

    User.room = message['room']
    print(message['room'])

@socketio.on('leave', namespace='/test')
def leave(message):         # leave

    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count'] },
         room= None )




@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    print('보내고싶다')
    print(rooms())
    if rooms() is not None:
        print('방있음')
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
            room=message['room'])
        print('방있네')
    else :
        print('방없음')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@socketio.on('close room', namespace='/test')
def close(message):         # close
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Room ' + message['room'] + ' is closing.',
          'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])



@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    #disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")
