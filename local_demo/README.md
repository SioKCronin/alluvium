# Local Demo Setup

## Play Cluster

* Start tweet firehose 'python tweets_producer.py'
* Run flask app 'python app/main.py'

## Storm Cluster

* Service Zookeeper (it will run in the background as a daemon)
* Service Storm nimbus, supervisor, and ui ('/usr/local/storm/bin/storm')
* Listen for queries 'python utils/query_builder.py'
