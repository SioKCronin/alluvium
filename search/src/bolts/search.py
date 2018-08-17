from streamparse import Bolt
import rethinkdb as r
from elasticsearch import Elasticsearch
import json
import time


class SearchBolt(Bolt):
    outputs = ['match_record']

    def initialize(self, stormconf, context):
        self.db = r.connect(host='ec2-54-202-215-9.us-west-2.compute.amazonaws.com', port='28015', db='alluvium')
        self.es = Elasticsearch()

    def process(self, tup):
        in_time = time.time()
        d = tup.values.doc[6]
        data = json.loads(d)
        doc = {
            "query" : {
                "percolate" : {
                    "field" : "query",
                    "document" : {
                        "message" : data['text']
                    }
                }
            }
        }

        res = self.es.search(index="my-index", doc_type="_doc", body=doc)

        # Write matches to RethinkDB
        if res['hits']['total'] > 0:
            for hit in res['hits']['hits']:
                new_match = r.table("queries").insert([{
                    "query_id": hit['_id'],
                    "tweet_id": data['tweet_id'],
                    "text": data['text'],
                    "time": int((time.time() - in_time)*1000)
                }]).run(self.db)
        #self.emit([res])
