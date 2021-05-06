# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : demo2_consume.py
# @Function : TODO

import kafka

demo3_config = {
    'kafka_host': 'localhost:9092',
    'kafka_topic': 'demo3',
    'kafka_group_1': 'demo3_group1',
    'kafka_group_2': 'demo3_group2'
}


def consume():
    consumer = kafka.KafkaConsumer(demo3_config['kafka_topic'],
                                   group_id=demo3_config['kafka_group_1'],
                                   bootstrap_servers=[demo3_config['kafka_host']])
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


