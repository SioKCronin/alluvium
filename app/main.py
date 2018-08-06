from flask import Flask, render_template
from flask_socketio import SocketIO, send


conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

producer = KafkaProducer(bootstrap_servers=conn)
# Send user queries to Kafka query topic

@socketio.on('message')
def handleMessage(msg):
    print('Term: ' + msg)
    producer.send('query', msg)

matches = KafkaConsumer('match', bootstrap_servers=conn)

@socketio.on('json')
def returnMatches(json): 
    # First parse the incoming match json
    #Match client id, and return the (article, author, time found)
    #Possibly use emit
    send(msg)

if __name__ == '__main__':
    socketio.run(app)
