import sys
import boto3
import boto
import json
import botocore
from ast import literal_eval
from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time
from streamparse.spout import Spout


class QueriesSpout(Spout):

    def intialize(self, stormconf, context):
        conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
        docs = KafkaConsumer('queries', bootstrap_servers=conn)

    def next_tuple(self):
        doc = next(self.docs)
        self.emit(doc)

    def ack(self, tup_id):
        pass

    def fail(self, tup_id):
        pass