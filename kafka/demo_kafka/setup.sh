#!/bin/bash
cd /opt/kafka/bin
echo "setup kafka!!!!"
#kafka-server-start.sh ../config/server.properties
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 1 --topic demo1
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 2 --topic demo2
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 4 --topic demo3
kafka-topics.sh --zookeeper demo_zookeeper:2181 --list
