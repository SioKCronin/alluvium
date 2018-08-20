from elasticsearch import Elasticsearch
import hashlib
from kafka import KafkaConsumer

#queries = ['love', 'hate', 'drunk']
es = Elasticsearch()

def build_query(q):
    query_term = q.value.decode("utf-8").strip()
    query_id = hashlib.md5(query_term.encode('utf-8')).hexdigest() 
    query =  {"query" : { "match" : {"message" : query_term}}}
    es.index(index="my-index", doc_type="_doc", body=query, id=query_id)

if __name__ == '__main__':
    conn = '10.0.0.14:9092'
    queries = KafkaConsumer('queries', bootstrap_servers=conn)
    for query in queries:
        build_query(query)

'''
If you encounter the following error:

raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)
elasticsearch.exceptions.AuthorizationException: TransportError(403, 'cluster_block_exception', 'blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];')

try this:

curl -X PUT "localhost:9200/my-index/_settings" -H 'Content-Type: application/json' -d' {"index": {"blocks": {"read_only_allow_delete": "false"}}}'

REF: https://discuss.elastic.co/t/forbidden-12-index-read-only-allow-delete-api/110282/4

or this:

curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

https://github.com/ankane/searchkick/issues/1040

'''
