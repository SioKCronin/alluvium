from streamparse import Bolt
import rethinkdb as r
from elasticsearch import Elasticsearch
import json
import time


class SearchBolt(Bolt):
    outputs = ['match_record']

    def initialize(self, stormconf, context):
        self.db = r.connect(host='10.0.0.11', port='28015', db='alluvium')
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
                    "user": data['user']['screen_name'],
                    "text": data['text'],
                    "timestamp": data['created_at']
                }]).run(self.db)
        self.emit([res])
