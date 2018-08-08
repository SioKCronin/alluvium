from elasticsearch import Elasticsearch

es = Elasticsearch()

query =  {"query" : { "match" : {"term" : "odio"}}}

es.index(index="my-index", doc_type = "_doc", body=query, id="test4")

'''
If you encounter the following error:

raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)
elasticsearch.exceptions.AuthorizationException: TransportError(403, 'cluster_block_exception', 'blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];')

try this:

curl -X PUT "localhost:9200/my-index/_settings" -H 'Content-Type: application/json' -d'
{
 "index": {
 "blocks": {
 "read_only_allow_delete": "false"
 }
 }
 }
'
REF: https://discuss.elastic.co/t/forbidden-12-index-read-only-allow-delete-api/110282/4
'''
