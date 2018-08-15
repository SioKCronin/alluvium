import sys
import json
from kafka import KafkaConsumer


if __name__ == "__main__":
    conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    queries = KafkaConsumer('queries', bootstrap_servers=conn)

    for query in queries:
        print(query.value.decode("utf-8").strip())
