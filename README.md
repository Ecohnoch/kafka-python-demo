# kafka-python-demo

这里放一些kafka的python的demos，目前（v1.0.1）有三个demo，三个demo跑通后即可基本的在python中使用kafka。

演示过程如下述。

### 第一步、本机启动Kafka服务

首先要下载docker和docker-compose。

不同操作系统的docker按照可以参考：[docker按照教程](https://www.runoob.com/docker/ubuntu-docker-install.html)

docker-compose可以直接用pip install docker-compose即可。

然后cd到本目录下的kafka中，使用docker-compose up构建zookeeper和kafka镜像并且启动容器。

启动后进入kafka容器的命令行，运行：

```shell
/bin/bash setup.sh
```

setup.sh的内容如下，也可以手动输入，主要是构建三个demo的主题（topic）。

```shell
#!/bin/bash
cd /opt/kafka/bin
echo "setup kafka!!!!"
#kafka-server-start.sh ../config/server.properties
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 1 --topic demo1
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 2 --topic demo2
kafka-topics.sh --create --zookeeper demo_zookeeper:2181 --replication-factor 1 --partitions 4 --topic demo3
kafka-topics.sh --zookeeper demo_zookeeper:2181 --list
```

### 第二步、测试demo1

demo1中测试的是一个topic，单个partition，单个consumer的情况，也就是传统的【队列模型】，只持有一个队列，生产者往这个队列中不停的生产消息，消费者从另一端不停的消费消息。

测试方法如下：

cd进入demo1的文件夹中，开两个终端，先在第一个终端运行python demo1_consume.py，看到'link kafka ok.'则表示消费者正在监听。

然后在第二个终端运行python demo1_produce.py，会很快的生产五个消息滨并且结束，在第一个终端中，可以看到消费者的消费结果：

```
link kafka ok.
msg1_key msg1_val topic: demo1, partition: 0, offset: 0
msg2_key msg2_val topic: demo1, partition: 0, offset: 1
msg3_key msg3_val topic: demo1, partition: 0, offset: 2
msg4_key msg4_val topic: demo1, partition: 0, offset: 3
msg5_key msg5_val topic: demo1, partition: 0, offset: 4
```

### 第二步、测试demo2

demo2中测试的是一个topic，多个partition，多个消费者（同组）的模型。demo2测试的是2个partition和2个消费者，这样生产者生产的消息，会根据内部的策略均匀分配到两个partition，并且【分别】被两个消费者消费。在这个策略下，生产者生产的一条消息，一直都只会被消费一次，而不会被重复消费。

测试方法如下：

cd进入demo1的文件夹中，开三个终端，先在第一个终端运行python demo2_consume.py，看到'link kafka ok.'则表示消费者正在监听。

然后在第二个终端运行python demo2_consume.py，看到'link kafka ok.'则表示第二个消费者正在监听。

然后在第三个终端运行python demo2_produce.py，会很快的生产五个消息滨并且结束，在两个消费者的终端中，会分别看到五个消息被两个消费者分别消费，并且顺序不能保证是生产的顺序：

生产者：

```
link kafka ok.
produce: key=msg1_key, val=msg1_val
produce: key=msg2_key, val=msg2_val
produce: key=msg3_key, val=msg3_val
produce: key=msg4_key, val=msg4_val
produce: key=msg5_key, val=msg5_val
produce over.
```

消费者1：
```
link kafka ok.
msg2_key msg2_val topic: demo2, partition: 0, offset: 0
msg4_key msg4_val topic: demo2, partition: 0, offset: 1
```

消费者2：

```
link kafka ok.
msg1_key msg1_val topic: demo2, partition: 1, offset: 0
msg3_key msg3_val topic: demo2, partition: 1, offset: 1
msg5_key msg5_val topic: demo2, partition: 1, offset: 2
```

### 第三步、测试demo3

demo3中测试的是一个topic，多个partition，多个消费者（有不同组）的模型。

demo3测试的是4个partition和3个消费者，其中2个消费者同组，1个消费者不同组，这样生产者生产的消息，会根据内部的策略均匀分配到四个partition，两个消费者组都订阅了这个topic。

第一个消费者组有2个消费者，会按照和之前的队列模型一样，分别消费两个分区的内容，消费的消息是互斥的，且两个消费者消费的消息的总和为生产者生产的所有消息。

第二个消费者组有1个消费者，会消费四个分区的内容，所以生产者生产的所有消息，也会完全的被第二个消费者组的这个消费者进行消费。

测试方法如下：

cd进入demo3的文件夹中，开四个终端，先在第一个终端运行python demo3_g1_consume1.py，看到'link kafka ok.'则表示消费者正在监听。

然后在第二个终端运行python demo3_g1_consume2.py，看到'link kafka ok.'则表示第二个消费者正在监听。

然后在第三个终端运行python demo3_g2_consume1.py，看到'link kafka ok.'则表示第三个消费者正在监听。

其中前两个消费者为一组，第三个消费者为一组。

然后在第四个终端运行python demo2_produce.py，会很快的生产五个消息滨并且结束，在前两个消费者的终端中，会看到和demo2类似的效果，而第三个消费者，则会完全的消费五条消息。

生产者：

```
link kafka ok.
produce: key=msg1_key, val=msg1_val
produce: key=msg2_key, val=msg2_val
produce: key=msg3_key, val=msg3_val
produce: key=msg4_key, val=msg4_val
produce: key=msg5_key, val=msg5_val
produce over.
```

消费者1（demo3_g1_consume1）：
```
link kafka ok.
msg5_key msg5_val topic: demo3, partition: 3, offset: 0
```

消费者2（demo3_g1_consume2）：

```
link kafka ok.
msg2_key msg2_val topic: demo3, partition: 0, offset: 0
msg4_key msg4_val topic: demo3, partition: 0, offset: 1
msg1_key msg1_val topic: demo3, partition: 1, offset: 0
msg3_key msg3_val topic: demo3, partition: 1, offset: 1
```

消费者3（demo3_g2_consume1）：

```
link kafka ok.
msg1_key msg1_val topic: demo3, partition: 1, offset: 0
msg3_key msg3_val topic: demo3, partition: 1, offset: 1
msg2_key msg2_val topic: demo3, partition: 0, offset: 0
msg4_key msg4_val topic: demo3, partition: 0, offset: 1
msg5_key msg5_val topic: demo3, partition: 3, offset: 0
```