 /usr/local/kafka/bin/kafka-producer-perf-test.sh --topic docs --num-records 1000000 --payload-file '/home/ubuntu/peg_log.txt' --throughput 10000 --producer-props bootstrap.servers=localhost:9092
