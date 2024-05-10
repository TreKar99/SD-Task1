#!/usr/bin/env python
import sys

import pika

from ConsumerThreadGroupChat import ConsumerThread

# Executing consumer in a thread
thread = ConsumerThread(sys.argv[1], sys.argv[2])
thread.start()

# Connection to RabbitMQ server
connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

group_name = sys.argv[1]

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
    print("\nEnding publisher...")
    thread.stop()

thread.join()
print("\nDo you want to unsubscribe the group? [Y/N]")
answer = input()
if answer == "Y":
    channel.queue_unbind(exchange=group_name, queue=sys.argv[2])
connection.close()
print("\nGroup chat left")
