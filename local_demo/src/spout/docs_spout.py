from kafka import KafkaConsumer
import time
from streamparse.spout import Spout


class DocsSpout(Spout):

    def intialize(self, stormconf, context):
        conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
        docs = KafkaConsumer('docs', bootstrap_servers=conn)

    def next_tuple(self):
        doc = next(self.docs)
        self.emit(doc)

    def ack(self, tup_id):
        pass

    def fail(self, tup_id):
        pass
