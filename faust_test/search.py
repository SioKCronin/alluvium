import faust
import rethinkdb as r
from elasticsearch import Elasticsearch

app = faust.App('stream_search', broker='kafka://ec2-52-13-241-228.us-west-2.compute.amazonaws.com:9092')
docs = app.topic('docs')
db = r.connect(host='ec2-54-202-215-9.us-west-2.compute.amazonaws.com', port='28015', db='alluvium')
es = Elasticsearch()

@app.agent(docs)
async def search(docs):
    async for doc in docs:
        # process stream
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
            print("Found match", new_match)

        else:
            print("Not match")

if __name__ == '__main__':
    app.main()
