# Alluvium

A realtime streaming search platform in Python. 

### Introduction
Alluvium provides a clean, scalable architecture in Python for realtime streaming search. Realtime search provides insight
into high velocity feeds, with applications ranging from media monitoring to up-to-date anti-vandelism detection
notifications.

Achieving realtime search in high volume streams presents a unique set of engineering challenges. 
For example, when we search in a static setting we typically create an index on the document we are searching, which is 
often not feasible in high-volume streams. This limitation led to the development of reverse search where queries are indexed 
and matched against a tokenized stream of text. Solme challenges emerge as additional queries are added. Should we tokenize
the streaming documents for each query, or tokenize them once and run them against several queries in batches? How should we 
remove queries from the list? How shall we scale the processing distribution to handle both an increase in document volume 
as well as an increase in number and complexity of queries? These are some of the questions I've been addressing with
Alluvium.

### Architecture
* **AWS (S3)**: Documents + queries
* **Kakfa**: Scalable, fault-tolerant message delivery
* **Storm**: Event-based stream processing
* **Elasticsearch**: Document indexing with Percolator queries
* **RethinkDB**: Data store
* **Flask-Socket.io**: Server socket connection to browser

### Twitter Data
* Sample JSON tweet data from a selection of the 300+ million registered users

### Engineering Challenges
* Kafka tuning
* Storm topology configuration and deployment in Python
* Pipeline metrics

### Performance
* Currently **200 registered queries** are found in an average of **40 milliseconds** in **1,000 records/second** stream.
