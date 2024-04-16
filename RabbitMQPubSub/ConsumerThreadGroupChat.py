#!/usr/bin/env python
import threading
import pika


class ConsumerThreadGroupChat(threading.Thread):
    def __init__(self, event):
        # Superclass constructor
        super(ConsumerThreadGroupChat, self).__init__()
        # Event
        self.event = event

    def run(self):
        # Connection to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='groupchat', exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='groupchat', queue=queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(f"Received [{body.decode('utf-8')}]")
            if body.decode('utf-8') == "EXIT":
                channel.stop_consuming()

        channel.basic_consume(queue=queue_name,
                              on_message_callback=callback,
                              auto_ack=True)

        while not self.event.is_set():
            channel.start_consuming()  # Only start consuming if not signaled to stop

        print("\nEnding consumer...")
