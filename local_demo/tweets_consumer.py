import sys
import json
from kafka import KafkaConsumer


if __name__ == "__main__":
    conn = 'ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092'
    docs = KafkaConsumer('docs', bootstrap_servers=conn)

    for msg in docs:
        data = json.loads(msg.value.decode("utf-8"))
        if 'delete' in data:
            pass
        else:
            print(data['text'])
