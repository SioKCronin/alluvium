import itertools

from streamparse.spout import Spout


class DocsSpout(Spout):
    outputs = ['doc']

    def initialize(self, stormconf, context):
        c = '10.0.0.14:9092'
        self.docs = KafkaConsumer('docs', bootstrap_servers=c)

    def next_tuple(self):
        doc = next(self.docs)
        self.emit([doc])

    def ack(self, tup_id):
        pass # add to log

    def fail(self, tup_id):
        pass # add to log
