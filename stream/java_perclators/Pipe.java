package myapps;

import org.apache.kafka.common.serializatddion.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;

properties streamsConfiguration = new Properties()

streamsConfiguration.put(APPLICATION_ID_CONFIG, "Streaming-QuickStart")
streamsConfiguration.put(BOOTSTRAP_SERVERS_CONFIG, "localhost:9092")
streamsConfiguration.put(DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String.getClass.getName)
streamsConfiguration.put(DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String.getClass.getName)

val builder = new KStreamBuilder
val kStream = builder.stream("docs")

//This is where we do our Elasticsearch
//EXAMPLE
val upperCaseKStream = kStream.mapValues(_.toUpperCase)
//characters of values are now converted to upper case
upperCaseKStream.to("OutTopic")
//sending data to out topic

//val stream = new KafkaStreams(builder, streamsConfiguration)
stream.start()
