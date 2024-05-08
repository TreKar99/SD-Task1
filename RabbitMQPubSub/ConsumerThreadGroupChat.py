import threading
import pika


class ConsumerThread(threading.Thread):
    def __init__(self, group_name):
        super(ConsumerThread, self).__init__()
        self._is_interrupted = False
        self.group_name = group_name

    def stop(self):
        self._is_interrupted = True
        print("\nEnding consumer...")

    def run(self):
        # Connection to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Exchange: group
        channel.exchange_declare(exchange=self.group_name, exchange_type='fanout', durable=True)

        result = channel.queue_declare(queue='', exclusive=True, durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.group_name, queue=queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        for message in channel.consume(queue_name, inactivity_timeout=1, auto_ack=False):
            if self._is_interrupted:
                break
            if not all(message):
                continue
            method, properties, body = message
            print(f"Received [{body.decode('utf-8')}]")
