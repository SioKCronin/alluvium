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

    # db connection
    # conn = r.connect(host='ec2-54-202-215-9.us-west-2.compute.amazonaws.com', port='28015', db='alluvium')
    conn = r.connect(host='10.0.0.11', port='28015', db='alluvium')

    # Listen to Kafka docs topic
    c = '10.0.0.14:9092'
    docs = KafkaConsumer('docs', bootstrap_servers=c)

    # Create Elasticsearch instance
    es = Elasticsearch()

    for msg in docs:
        #print(msg.value.decode("utf-8"))
        data = json.loads(msg.value.decode("utf-8"))
        #data = json.loads(msg.value.strip(',').decode("utf-8"))
        print(data)

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

        print(res)

        # Write matches to RethinkDB
        if res['hits']['total'] > 0:
            match = json.loads(msg.value.decode('utf-8').strip(','))
            #print(match)
            for hit in res['hits']['hits']:
                print("Found one!")
                found_match = r.table("queries").insert([{
                    "query_id": hit['_id'],
                    "article": match['article'],
                    "user_id": match['user_id'],
                    "time": time.time()
                }]).run(conn)
                print(found_match)

        else:
            pass
            #print("Not match")
