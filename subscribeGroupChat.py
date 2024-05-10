#!/usr/bin/env python
import sys

import pika

# Subscribe in a group
# Connection to RabbitMQ server
connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

group_name = sys.argv[1]

channel.exchange_declare(exchange=group_name, exchange_type='fanout', durable=True)

queue_name = sys.argv[2]

channel.queue_declare(queue=queue_name, durable=True)

channel.queue_bind(exchange=group_name, queue=queue_name)

print(f"Client subscribed to [{group_name}]")