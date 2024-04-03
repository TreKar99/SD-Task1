#!/usr/bin/env python
import pika
import time

import signal

from threading import Thread


class Consumer(Thread):

    def run(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = self.connection.channel()
            channel.queue_declare(queue='insult_channel')  # , durable=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.basic_consume(queue='insult_channel',
                                  on_message_callback=self.callback)
            channel.start_consuming()
        except:
            pass
        finally:
            if self.connection:
                self.connection.close()
            print("Saliendo")

    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

