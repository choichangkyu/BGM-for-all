#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, make_response, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

room_name=None



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comment')
def comment():

    return render_template('comment.html')


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

@socketio.on('join', namespace='/test')
def join(message):          # join
    if message['room'] is not ' ':
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

    #print(rooms())
    #print(message['room'])

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
