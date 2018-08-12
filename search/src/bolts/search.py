import os
from collections import Counter

from streamparse import Bolt


class SearchBolt(Bolt):
    outputs = ['match_record']

    def initialize(self):
        self.db = r.connect(host='10.0.0.11', port='28015', db='alluvium')
        self.es = Elasticsearch()
        self.total = 0

    def process(self, tup):
        doc = tup.values[0]
        data = json.loads(doc.value.decode("utf-8").rstrip(','))
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
            match = json.loads(doc.value.decode('utf-8').strip(','))
            for hit in res['hits']['hits']:
                new_match = self.db.table("queries").insert([{
                    "query_id": hit['_id'],
                    "article": match['article'],
                    "user_id": match['user_id']
                }]).run(conn)
                print("Found match",new_match)

        else:
            print("Not match")
