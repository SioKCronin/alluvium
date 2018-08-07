import sys
import json
import time
import os
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch


conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
term = "tired"

if __name__ == "__main__":

    docs = KafkaConsumer('docs', bootstrap_servers=conn)
    queries = KafkaConsumer('queries', bootstrap_servers=conn)
    producer = KafkaConsumer('match', bootstrap_servers=conn)

    # Create an inverted index

    #for query in queries:
    #  add to inverted index

    for msg in docs:
        data = json.loads(msg.value.decode("utf-8"))
        print(data['tokens'])
        if term in data['tokens']:
            print("Found it in {} ms".format(int(round(time.time() * 1000)) - msg.timestamp))
            # This is where you would send to Redis the info)
