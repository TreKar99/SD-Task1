#!/usr/bin/env python
import pika
import sys


class Producer:
	connection
	channel

	def __init__(self):
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	    self.channel = connection.channel()
	    self.channel.queue_declare(queue='insult_channel')
	
	def send(self):
		message = input('INSULTAME: ')  
		channel.basic_publish(
		    exchange='',
    routing_key='insult_channel',
    body=message
    #properties=pika.BasicProperties(
    #    delivery_mode=pika.DeliveryMode.Persistent
    )
		print(f" [x] Sent {message}")
		#connection.close()

	def close(self):
		
