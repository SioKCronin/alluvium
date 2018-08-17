import itertools

from streamparse.spout import Spout
from kafka import KafkaConsumer


class DocsSpout(Spout):
    outputs = ['doc']

    def initialize(self, stormconf, context):
        c = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com'
        self.docs = KafkaConsumer('tweets', bootstrap_servers=c)

    def next_tuple(self):
        doc = next(self.docs)
        self.emit([doc])

    '''
    def ack(self, tup_id):
        pass # add to log

    def fail(self, tup_id):
        pass # add to log
    '''
