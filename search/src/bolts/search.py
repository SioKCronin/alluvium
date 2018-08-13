from streamparse import Bolt
import rethinkdb as r
from elasticsearch import Elasticsearch
import json


class SearchBolt(Bolt):
    outputs = ['match_record']

    def initialize(self, stormconf, context):
        self.db = r.connect(host='ec2-54-202-215-9.us-west-2.compute.amazonaws.com', port='28015', db='alluvium')
        self.es = Elasticsearch()
        self.total = 0

    def process(self, tup):
        d = tup.values.doc[6].rstrip(',')
        data = json.loads(d)
        doc = {
            "query" : {
                "percolate" : {
                    "field" : "query",
                    "document" : {
                        "message" : data['revision']
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
                    "article": data['article'],
                    "user_id": data['user_id']
                }]).run(self.db)
        self.emit([res])
