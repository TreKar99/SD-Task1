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
            id_client_destinatari = int(
                input("Introdueix l'id del client amb el que vols iniciar el xat: "))

            # Redis ID
            r = redis.StrictRedis(host=redis_host, port=redis_port,
                                  password=redis_password, decode_responses=True)
            r.hset('private_chats', id_client, 'localhost')

            thread_lector = threading.Thread(target=funcio_llegir,
                                             args=(id_client, stub,),)
            thread_escriptor = threading.Thread(target=funcio_escriure,
                                                args=(id_client, id_client_destinatari, stub,),)
            thread_lector.start()
            thread_escriptor.start()

            thread_lector.join()
            thread_escriptor.join()
        except:
            # Redis ID
            r.hdel('private_chats', id_client)

            print("Tancant el chat privat")


def funcio_llegir(id_client, stub):
    flux_llegit = stub.RebreMissatges(
        chatPrivat_pb2.Client(id_destinatari=id_client))
    for missatge in flux_llegit:
        print(f"\r{missatge.id_remitent}: {missatge.missatge}")


def funcio_escriure(id_client, id_destinatari, stub):
    while True:
        missatge = input()

        stub.EnviarMissatge(chatPrivat_pb2.PeticioMissatge(
            id_thread=1, missatge=missatge, id_remitent=id_client, id_destinatari=id_destinatari,))

        if missatge == "EXIT":
            break


if __name__ == "__main__":
    logging.basicConfig()
    run()
