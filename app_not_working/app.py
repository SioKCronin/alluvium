import hashlib
import redis
from flask import Flask, session, render_template
from flask_socketio import SocketIO, send
from query_subscriber import QuerySubscriber
from views import attach_views
from datetime import datetime
from kafka import KafkaProducer

class AlluviumAppBase:

    def __init__(self, config):

        conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'mysecret'
        socketio = SocketIO(app)

        # attach a redis connection pool
        app.pool = redis.ConnectionPool(host="localhost", port=6379)

        @app.route('/')
        def index():
            return render_template('index.html')

        producer = KafkaProducer(bootstrap_servers=conn)

        socketio.on('message')
        def handleMessage(msg):
            hashed_query = hashlib.sha224(msg).hexdigest()
            print('Term: ' + msg)
            producer.send('query', hashed_query)

        # user -> channels mapping
        app.user_channels = {}

        def redis_message_handler(msg):    

            redis_connection = redis.Redis(connection_pool=app.pool)
            channel = msg['channel']
            data = msg['data']

            # word highlighting
            query = redis_connection.get(channel)
            words = list(set(query.split(" ")))
            for w in words:
                data=data.lower().replace(w.lower(), highlight(w.lower()))

            # find users subscribed to this channel
            if app.user_channels.get(channel) is not None:
                for user in app.user_channels.get(channel):
                    redis_connection.lpush(user, data)
            else:
                # no more users for this channel, unsubscribe from it
                redis_connection.unsubscribe(channel)

            # Add Redis query subscriber to app
            app.disp = []
            app.subscriber = QuerySubscriber("localhost", 6379, redis_message_handler)

            # setup kafka producer in the app
            kafka = KafkaClient("{0}:{1}".format(config["zookeeper_host"], 9092))
            app.producer = SimpleProducer(kafka)

        # add the app
        self.app = app

        def clear_user(self, uid):
            redis_connection = redis.Redis(connection_pool=self.app.pool)
            # find all the queries to which the user is subscribed
            # and remove them from the subscribers list for each query.
            for qid in redis_connection.lrange(uid+"-queries", 0, -1):
                try:
                    self.app.user_channels[qid].remove(uid)
                except KeyError:
                    pass

            # remove the user-queries
            redis_connection.delete(uid+"-queries")

            # remove the stored results
            redis_connection.delete(uid)

def get_alluvium_app(config):
    base = AlluviumAppBase(config)
    app = base.app
    attach_views(app)
    return app
