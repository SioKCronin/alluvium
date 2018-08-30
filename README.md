![sample](https://github.com/SioKCronin/alluvium/blob/master/media/sample_results.png)

# Alluvium
A scalable realtime streaming search platform

[DEMO](https://drive.google.com/file/d/12r1yYzYH6fVG5--n2Bxet_4_8Loi1dbs/view)

## Overview
Alluvium provides a clean, scalable architecture in Python for realtime streaming search. Realtime search provides insight
into high velocity feeds, with applications ranging from media monitoring to up-to-date anti-vandelism detection
notifications. A practical example would monitoring community health by tracking the frequency of words in the Twitte feed 
that correlate with heart disease mortality rates, as presented by [Eichstaedt et al](http://journals.sagepub.com/doi/abs/10.1177/0956797614557867) in 2015. 

Achieving realtime search in high volume streams presents a unique set of engineering challenges. 
For example, when we search in a static setting we typically create an index on the document we are searching, which is 
often not feasible in high-volume streams. This limitation led to the development of reverse search where queries are indexed 
and matched against a tokenized stream of text. Solme challenges emerge as additional queries are added. Should we tokenize
the streaming documents for each query, or tokenize them once and run them against several queries in batches? How should we 
remove queries from the list? How shall we scale the processing distribution to handle both an increase in document volume 
as well as an increase in number and complexity of queries? These are some of the questions I've been addressing with
Alluvium.

## Architecture
* **AWS (S3)**: Simulated firehose of tweets from 2012
* **Kakfa**: Scalable, fault-tolerant message delivery
* **Storm**: Event-based stream processing
* **Elasticsearch**: Tweet search with percolator index
* **RethinkDB**: Key-value data store
* **Flask-Socket.io**: Server socket connection deivering real-time results to client

## Engineering Challenges
* Kafka tuning
* Storm topology configuration and deployment in Python
* Pipeline metrics

## Performance monitoring
* Currently clocking an average of **4 milliseconds per search** on a **2000 tweets/second** stream.
