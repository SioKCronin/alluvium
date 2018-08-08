from elasticsearch import Elasticsearch

es = Elasticsearch()

doc = {
    "query" : {
        "percolate" : {
            "field" : "query",
            "document" : {
                "message" : "A new bonsai tree in the office"
            }
        }
    }
}

res = es.search(index="my-index", doc_type="_doc", body=doc)

print(res)
