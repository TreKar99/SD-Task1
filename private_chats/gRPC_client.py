import logging
import threading
import grpc

import chatPrivat_pb2
import chatPrivat_pb2_grpc

import redis
redis_host = "localhost"
redis_port = 6379
redis_password = ""


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        try:
            stub = chatPrivat_pb2_grpc.PrivateChatsServiceStub(channel)
            id_client = int(input("Introdueix el teu id: "))
            id_client_destinatari = int(input("Introdueix l'id del client amb el que vols iniciar el xat: "))

            # Redis ID
            r = redis.StrictRedis(host=redis_host, port=redis_port,
                                  password=redis_password, decode_responses=True)
            r.hset('private_chats', id_client, 'localhost')

            # Crear un thread que s'encarregarà de la lectura de missatges
            thread_lector = threading.Thread(target=funcio_llegir, args=(id_client, stub,),)
            # Crear altre thread que s'encarregarà de l'escriptura de missatges
            thread_escriptor = threading.Thread(target=funcio_escriure, args=(id_client, id_client_destinatari, stub,),)

            # Iniciar els dos threads
            thread_lector.start()
            thread_escriptor.start()

            thread_lector.join()
            thread_escriptor.join()
        except:
            # Redis ID
            r.hdel('private_chats', id_client)

            print("Tancant el xat privat")


# Funció que llegeix els missatges rebuts mostrant-los per pantalla
def funcio_llegir(id_client, stub):
    print(f"Dins del xat, per abandonar-lo introduir 'EXIT'")
    lectura_rebuda = stub.RebreMissatges(chatPrivat_pb2.Client(id_destinatari=id_client))
    for missatge in lectura_rebuda:
        print(f"\r[{missatge.id_remitent}]: {missatge.missatge}")


# Funció que envia el missatge escrit per pantalla al destinatari
def funcio_escriure(id_client, id_destinatari, stub):
    while True:
        missatge = input()

        stub.EnviarMissatge(chatPrivat_pb2.PeticioMissatge(id_thread=1, missatge=missatge, id_remitent=id_client, id_destinatari=id_destinatari,))

        # En cas que el missatge sigui 'EXIT' és indicatiu que el client vol abandonar el xat
        if missatge == "EXIT":
            break


if __name__ == "__main__":
    logging.basicConfig()
    run()
