from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from threading import Thread
import rethinkdb as r
from kafka import KafkaProducer
import json
from datetime import datetime
import hashlib

app = Flask(__name__)
socketio = SocketIO(app)
global thread
thread = None

# Kafka host
conn = '10.0.0.14:9092'
producer = KafkaProducer(bootstrap_servers=conn)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='secret!',
    DB_HOST='10.0.0.11',
    DB_PORT=28015,
    DB_NAME='alluvium'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

'''
Don't need these: 
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
'''

@app.route('/search', methods=['GET'])
def create_search():
    data = {}
    data['query'] = request.args.get('q', '')
    #data['created'] = datetime.now(r.make_timezone('00:00'))
    if data.get('query'):
        data['query_id'] = hashlib.md5(data['query'].encode('utf-8')).hexdigest()
        session['query_id'] = data['query_id']
        # Publish data to Kafka queries topic
        producer.send("queries", bytes(data['query']))
        #new_chat = r.table("queries").insert([ data ]).run(g.db_conn)
        return render_template('search.html', query=data['query'], room=data['query_id'])
    return make_response('no search param', 401)

@socketio.on('connect')
def test_connect():
    join_room(session['query_id'])

@socketio.on('disconnect')
def test_disconnect():
    if app.config['DEBUG']:
        print('Client disconnected')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def watch_results():
    print('Watching db for new results from db!')
    conn = r.connect(host=app.config['DB_HOST'],
                     port=app.config['DB_PORT'],
                     db=app.config['DB_NAME'])
    feed = r.table("queries").changes().run(conn)
    for result in feed:
        if app.config['DEBUG']:
            print("Found it")
            print(result)
        #result['new_val']['created'] = str(result['new_val']['created'])
        # emit to a specific client the results when they come into
        # rethinkdb for that client's query.
        socketio.emit('new_result', result, room=result['new_val']['query_id'])

if __name__ == "__main__":
    # Set up rethinkdb changefeeds before starting server
    if thread is None:
        thread = Thread(target=watch_results)
        thread.start()
    socketio.run(app, host='0.0.0.0', port=8000)
