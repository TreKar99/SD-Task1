#!/usr/bin/env python
import pika
#from inputBox import *


class Producer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='insult_channel')

    def send(self):
#        try:
            #            input = InputBox()
            #            message = input.input()
            message = input("INSULTAME ")
            self.channel.basic_publish(
                exchange='',
                routing_key='insult_channel',
                body=message
            )
            print(f" [x] Sent {message}")
#        finally:
#            self.close()

    def close(self):
        self.connection.close()
