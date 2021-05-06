import kafka

demo1_config = {
    'kafka_host': 'localhost:9092',
    'kafka_topic': 'demo1'
}

def consume():
    consumer = kafka.KafkaConsumer(demo1_config['kafka_topic'],
                                   bootstrap_servers=[demo1_config['kafka_host']])
    print('link kafka ok.')
    for msg in consumer:
        this_key_bytes = msg.key
        this_val_bytes = msg.value

        this_key = str(this_key_bytes, encoding='utf-8')
        this_val = str(this_val_bytes, encoding='utf-8')
        #  msg.key, msg.value, msg.topic, msg.partition, msg.offset
        print(this_key, this_val, 'topic: {}, partition: {}, offset: {}'.format(msg.topic, msg.partition, msg.offset))

if __name__ == '__main__':
    consume()


