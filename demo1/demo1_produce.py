import kafka

demo1_config = {
    'kafka_host': 'localhost:9092',
    'kafka_topic': 'demo1'
}


def produce():
    producer = kafka.KafkaProducer(bootstrap_servers=[demo1_config['kafka_host']])
    print('link kafka ok.')

    messages = [
        {'msg1_key': 'msg1_val'},
        {'msg2_key': 'msg2_val'},
        {'msg3_key': 'msg3_val'},
        {'msg4_key': 'msg4_val'},
        {'msg5_key': 'msg5_val'}]

    for each_msg in messages:
        this_key = list(each_msg.keys())[0]
        this_val = each_msg[this_key]
        future = producer.send(demo1_config['kafka_topic'], key=this_key.encode('utf-8'),value=this_val.encode('utf-8'))
        print('produce: key={}, val={}'.format(this_key, this_val))
    producer.close()
    print('produce over.')

if __name__ == '__main__':
    produce()


