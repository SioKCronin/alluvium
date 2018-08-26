from streamparse.bolt import Bolt
from elasticsearch import Elasticsearch
import sys
import json
import time
import os
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from streamparse.bolt import Bolt

class QuerySearchBolt(Bolt):

    #conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    conn = '10.0.0.14:9092'
    docs = KafkaConsumer('docs', bootstrap_servers=conn)
    producer = KafkaConsumer('match', bootstrap_servers=conn)
    es = Elasticsearch()

    def process(self, tup):
        data = json.loads(tup.value.decode("utf-8").strip(','))

        doc = {
            "query" : {
                "percolate" : {
                    "field" : "query",
                    "document" : {
                        "message" : "{}".format(data['revision'])
                    }
                }
            }
        }

        res = es.search(index="my-index", doc_type="_doc", body=doc)
        #If match - write do RethinkDB
        print(res)
