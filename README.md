# alluviam

Realtime streaming search with Kafka Streams

### Introduction
Alluviam provides a clean, scalable architecture for real-time search on streaming text. Realtime search can 
provide companies with the ability to monitor high velocity text feeds, with applications ranging from media
monitoring to anti-vandelism/abuse detection.

Achieving near real-time search in high volume streaming text data presents a unique set of engineering challenges. For example, 
when we search in a static setting we typically create an index, which is often not feasible in high velocity streaming docs. 
This limitation led to the development of reverse search strategies where queries are indexed and matched against a tokenized 
stream of text. Challenges emerge as additional processing is added beyond identifying matches, as well as handling complex 
queries, and it is these edge cases that alluviam seeks to address. 

### Architecture
* **AWS (S3)**: Docs + Queries (simulated data firehoses)
* **Kakfa Streams**: Scalable, fault-tolerant, low-latency streaming
* **Elasticsearch**: Document tokenization + text indexing (Percolator queries)
* **Flask-Socket.io**: Server socket connection to browser

### Dataset
* 31 million registered users, although only about 119K active users making at least 1 edit/month
* 1TB of Wikipedia revision log data (xml archive dump)
* 10-20 changes/second from the RCFeed (can speed up using the historical data for velocity)
* 29 million pages (reduce to 10 million that are in the encyclopedia, and 4.2 million are articles, stubs and 
disambiguation pages) 
* All data from inception to 2008: https://snap.stanford.edu/data/wiki-meta.html
* Archived data: https://dumps.wikimedia.org/enwiki/latest/

### Engineering Challenges
* Decouple the scalability, the latency, and the availability of our stream processing application with an external database
* Elasticsearch integration with Kafka Streams
* Producer tuning (compression, batch size) 
* Broker tuning (leader balancing)
* Consumer tuning

#### Specs/Constraints
* Presently, can return match results at a rate of 0 records/second (room for improvement!)
