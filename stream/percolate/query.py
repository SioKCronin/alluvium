from elasticsearch import Elasticsearch
import sys
import json
import time
import os
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'

if __name__ == "__main__":

    docs = KafkaConsumer('docs', bootstrap_servers=conn)
    producer = KafkaConsumer('match', bootstrap_servers=conn)

    es = Elasticsearch()

    for msg in docs:
        data = json.loads(msg.value.decode("utf-8").strip(','))

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
        print(res)
