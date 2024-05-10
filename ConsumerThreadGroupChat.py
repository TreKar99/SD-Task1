import threading
import pika


class ConsumerThread(threading.Thread):
    def __init__(self, group_name, queue_name):
        super(ConsumerThread, self).__init__()
        self._is_interrupted = False
        self.group_name = group_name
        self.queue_name = queue_name

    def stop(self):
        self._is_interrupted = True
        print("\nEnding consumer...")

    def run(self):
        # Connection to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        print(' [*] Waiting for logs. To exit press CTRL+C')

        for message in channel.consume(self.queue_name, inactivity_timeout=1, auto_ack=True):
            if self._is_interrupted:
                break
            if not all(message):
                continue
            method, properties, body = message
            print(f"Received [{body.decode('utf-8')}]")
