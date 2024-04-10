#!/usr/bin/env python
import pika

class Producer:

    def __init__(self, ip):
        self.ip = ip
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='insult_channel')

    def send(self):
        message = input("INSULTAME ")
        self.channel.basic_publish(
            exchange='',
            routing_key='insult_channel',
            body=message
        )
        print(f" [x] Sent {message}")

    def close(self):
        self.connection.close()
