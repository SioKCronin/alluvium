import sys
import boto3
import boto
import json
import botocore
from ast import literal_eval
from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time


def main():

    conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    producer = KafkaProducer(bootstrap_servers=conn)

    for i in range(1000):
        print(int(time.time()))
        for line in smart_open('s3://alluvium-data/mvp_docs.json'):
            #print(line.strip())
            producer.send('docs', line.strip())
            producer.flush()
            time.sleep(.01)

if __name__ == '__main__':
    main()