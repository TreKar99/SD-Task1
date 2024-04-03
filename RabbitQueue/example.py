from queueClassServerRabbit import *
from queueClassClientRabbit import *

import signal

try:
    c = Consumer()
    c.start()
    try:
        while True:
            p = Producer()
            p.send()
    except KeyboardInterrupt:
        p.close()
        print("Saliendo cliente")
    c.join()
except KeyboardInterrupt:
    print("Salida del programa")
except pika.exceptions.AMQPConnectionError as e:
    print("Error de conexión a RabbitMQ:", e)
except pika.exceptions.ChannelClosed as e:
    print("Canal cerrado:", e)
