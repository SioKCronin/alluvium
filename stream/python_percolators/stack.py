from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient

client = Elasticsearch([{'host': 'localhost', 'port': 9200}])
ies = IndicesClient(client)

mapping = {
  "mappings": {
    "my-type": {
      "properties": {
        "content": {
          "type": "string"
        }
      }
    }
  }
}

ies.create(index='test_index', body=mapping)

query = {
    "query": {
        "match": {
            "content": "python"
        }
    }
}
es.create(index='test_index', doc_type='.percolator', body=query, id='python')

doc1 = {'doc': {'content': 'this is something about python'}}
res = es.percolate("test_index", doc_type="my-type", body = doc1)
print(res)

# result:
# {u'matches': [{u'_id': u'python', u'_index': u'test_index'}], u'total': 1, u'took': 3, u'_shards': {u'successful': 5, u'failed': 0, u'total': 5}}

doc2 = {'doc': {'content': 'this is another piece of text'}}
res = es.percolate("test_index", doc_type="my-type", body = doc2)
print(res)
# result:
# {u'matches': [], u'total': 0, u'took': 2, u'_shards': {u'successful': 5, u'failed': 0, u'total': 5}}
