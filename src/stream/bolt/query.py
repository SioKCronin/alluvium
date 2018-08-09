from elasticsearch import Elasticsearch
import sys
import json
import time
import os
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import rethinkdb as r
import hashlib


if __name__ == "__main__":

    # ThinkDB connection
    conn = r.connect()

    # Listen to Kafka docs topic
    c = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    docs = KafkaConsumer('docs', bootstrap_servers=c)

    # Create Elasticsearch instance
    es = Elasticsearch()

    for msg in docs:
        data = json.loads(msg.value.decode("utf-8").strip(','))

        doc = {
            "query" : {
                "percolate" : {
                    "field" : "query",
                    "document" : {
                        "message" : data['revision']
                    }
                }
            }
        }

        res = es.search(index="my-index", doc_type="_doc", body=doc)

        # Write matches to RethinkDB
        if res['hits']['total'] > 0:
            for hit in res['hits']['hits']:
                print("Found one!")
                r.table("queries").insert({
                    query_id: hit['_id'],
                    article: data['article'],
                    user_id: data['user_id']
                }).run(conn, callback)

        else:
            print("Not match")
