import sys
import json
from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time


def main():

    conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    producer = KafkaProducer(bootstrap_servers=conn)
    t = time.time() * 1000
    count = 0

    while True:
        #print("Time:",(time.time()*1000) - t)

        for line in smart_open('s3://alluvium-data/cleaned_tweets.json'):
            if count % 1000 == 0:
                print("Count:", count,"at time diff:", time.time()*1000 - t)
            count += 1
            #data = json.loads(line.decode("utf-8").strip())
            producer.send('tweets', line)
        producer.flush()
        #time.sleep(.01)

if __name__ == '__main__':
    main()
