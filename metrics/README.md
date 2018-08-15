## Kafka

To monitor our Kafka cluster, we can use a module called jconsole that comes with java
It has a GUI we can run on our local machine that connects into the servers. Here's 
more [information](https://docs.oracle.com/javase/7/docs/technotes/guides/management/jconsole.html) on how to connect and what's provided.

By default the management API only runs within the local network on EC2, 
so you can't access it remotely. One way around this is to set up an SSH tunnel into 
the specific ports used by the remote management interface. If you're using Insight's 
Pegasus project, you can use `peg port-forward` to do exactly the same thing as the SS
tunnel.

## Storm

Storm UI runs on port 8080 on Nimbus. You just need an SSH port forward on that 
machine in order to see it. You should be able to monitor it from there.

## Elasticsearch

One way to monitor Elasticsearch is with a package called 
[Kibana](https://www.elastic.co/guide/en/kibana/current/setup.html). It will 
create a web interface you can connect to and will need an SSH port forward to.

## Rethinkdb

That same SSH tunnel technique is how you can also connect to the rethinkdb 
administrative website. You just need to tunnel rethinkdb's website 
(port 8080 on the EC2 instance) to your local machine and load up localhost 
(whatever port number you choose) locally.
