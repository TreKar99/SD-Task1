#!/usr/bin/env python
import sys

import pika

from ConsumerThreadGroupChat import ConsumerThread

import redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""

# Executing consumer in a thread
thread = ConsumerThread(sys.argv[1])
thread.start()

# Connection to RabbitMQ server
connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

group_name = sys.argv[1]

# Redis ID
r = redis.StrictRedis(host=redis_host, port=redis_port,password=redis_password, decode_responses=True)
r.hset('group_chats', group_name, 'localhost')

channel.exchange_declare(exchange=group_name, exchange_type='fanout', durable=True)

# Executing publisher
# Loop publisher
try:
    while True:
        message = input()

        channel.basic_publish(exchange=group_name, routing_key='', body=message, properties=pika.BasicProperties(
                         delivery_mode=pika.DeliveryMode.Persistent
                      ))
        print(f"Sent [{message}]")
except KeyboardInterrupt:
    # Redis ID
    r.hdel('group_chats', group_name)
    print("\nEnding publisher...")
    thread.stop()

thread.join()
connection.close()
print("\nGroup chat left")
