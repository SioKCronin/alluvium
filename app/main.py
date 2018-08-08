from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from threading import Thread
import rethinkdb as r
from rethinkdb import RqlRuntimeError
import json
from datetime import datetime
import hashlib

app = Flask(__name__)
socketio = SocketIO(app)
global thread
thread = None

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret!',
    DB_HOST='localhost',
    DB_PORT=28015,
    DB_NAME='chat'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    try:
        g.db_conn = r.connect(host=app.config['DB_HOST'],
                              port=app.config['DB_PORT'],
                              db=app.config['DB_NAME'])
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.db_conn.close()
    except AttributeError:
        pass

@app.route('/search', methods=['GET'])
def create_search():
    data = {}
    data['query'] = request.args.get('q', '')
    data['created'] = datetime.now(r.make_timezone('00:00'))
    data['room'] = hashlib.md5(data['query'].encode('utf-8')).hexdigest()
    if data.get('query'):
        # kick off the search process -- send query to Kafka producer
        new_chat = r.table("chats").insert([ data ]).run(g.db_conn)
        return render_template('search.html', query=data['query'], room=data['room'])
    return make_response('no search param', 401)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    send('Someone has entered the room.', room=room)

# TODO: When socket disconnects, remove query from db (or set a timer)?

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def watch_results():
    print('Watching db for new results from db!')
    conn = r.connect(host=app.config['DB_HOST'],
                     port=app.config['DB_PORT'],
                     db=app.config['DB_NAME'])
    feed = r.table("chats").changes().run(conn)
    for result in feed:
        result['new_val']['created'] = str(result['new_val']['created'])
        # emit to a specific client the results when they come into
        # rethinkdb for that client's query.
        socketio.emit('new_result', result)

if __name__ == "__main__":
    # Set up rethinkdb changefeeds before starting server
    if thread is None:
        thread = Thread(target=watch_results)
        thread.start()
    socketio.run(app, host='0.0.0.0', port=8000)
