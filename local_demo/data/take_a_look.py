from smart_open import smart_open, s3_iter_bucket
from kafka import KafkaProducer
import time

def main():

    for line in smart_open('s3://wikipedia-raw-xml-data/sample_docs.xml'):
        print(line)
        time.sleep(.01)

if __name__ =='__main__':
    main()
