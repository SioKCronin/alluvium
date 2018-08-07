import sys
import boto3
import boto
import json
import botocore
from ast import literal_eval
from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time

conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'

def main():

    producer = KafkaProducer(bootstrap_servers=conn)

    #Keep it looping: for i in 1000:
    for line in smart_open('s3://alluvium-data/mvp_docs.json'):
        print(line)
        producer.send('docs', line)
        producer.flush()
        #time.sleep(1)

if __name__ == '__main__':
    main()
