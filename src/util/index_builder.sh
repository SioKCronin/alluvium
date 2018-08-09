# When setting a new index

curl -X PUT "localhost:9200/latin-index" -H 'Content-Type: application/json' -d'
{
    "mappings": {
        "_doc": {
            "properties": {
                "message": {
                    "type": "text"
                },
                "query": {
                    "type": "percolator"
                }
            }
        }
    }
}
'

