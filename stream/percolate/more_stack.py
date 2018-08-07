from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

query = {'query': {'usr': {'term': 'lovely'}}}
es.create(index='test', doc_type='percolator', body=query, id='python')
doc = {'doc': {'message': 'It is a lovely day'}}
k = es.percolate(index='test', doc_type='type1', body=doc)

print(k)
