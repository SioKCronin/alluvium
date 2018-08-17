import sys
import boto3
import boto
import json
from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time


def main():

    conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    producer = KafkaProducer(bootstrap_servers=conn)

    for line in smart_open('s3://alluvium-data/sample_tweets.json'):
        data = json.loads(line.decode("utf-8").strip())
        if 'delete' in data:
            continue
        else:
            producer.send('tweets', {'tweet_id': data['id_str'],
                                     'text': data['text']})
            producer.flush()
            time.sleep(.01)

if __name__ == '__main__':
    main()
