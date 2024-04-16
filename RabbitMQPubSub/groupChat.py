#!/usr/bin/env python
import sys
import pika
from threading import Event

from ConsumerThreadGroupChat import ConsumerThreadGroupChat

# Create an event
event = Event()

# Executing consumer in a thread
thread = ConsumerThreadGroupChat(event)
thread.start()

# Connection to RabbitMQ server
connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='groupchat', exchange_type='fanout')

# Executing publisher
# Loop publisher
try:
    while True:
        message = input()

        channel.basic_publish(exchange='groupchat', routing_key='', body=message)
        print(f"Sent [{message}]")
except KeyboardInterrupt:
    print("\nEnding publisher...")
    channel.basic_publish(exchange='groupchat', routing_key='', body="EXIT")
    event.set()

thread.join()
connection.close()
print("\nGroup chat left")



