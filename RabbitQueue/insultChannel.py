from queueClassServerRabbit import *
from queueClassClientRabbit import *

from time import sleep

try:
    c = Consumer('localhost')
    c.start()
    try:
        while True:
            sleep(0.2)
            p = Producer('localhost')
            p.send()
    except KeyboardInterrupt:
        p.close()
        print("\nSaliendo cliente")
    c.join()
except KeyboardInterrupt:
    print("\nSalida del programa")
except pika.exceptions.AMQPConnectionError as e:
    print("Error de conexión a RabbitMQ:", e)
except pika.exceptions.ChannelClosed as e:
    print("Canal cerrado:", e)
