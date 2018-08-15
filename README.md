# Alluvium

Real-time streaming search in Python. 

### Introduction
Alluvium provides a clean, scalable architecture in Python for real-time streaming search. Real-time search provides insight
into high velocity  feeds, with applications ranging from media monitoring to up-to-date anti-vandelism/abuse detection.

Achieving real-time search in high volume streams presents a unique set of engineering challenges. 
For example, when we search in a static setting we typically create an index, which is often not feasible in high 
velocity streaming docs. This limitation led to the development of reverse search strategies where queries are indexed 
and matched against a tokenized stream of text. Challenges emerge as additional queries are added. Should we tokenize
stream for each query, or run them in batches? How do we remove queries from the search list? How do we scale the processing
to handle both an increase in document volume as well as an increase in number and complexity of queries? These are some of
the questions Alluvium seekds to to address.

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
* Currently **200 registered queries** found in an average of **40 milliseconds** in stream of **1,000 records/second**
