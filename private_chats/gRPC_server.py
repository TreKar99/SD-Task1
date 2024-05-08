import asyncio
import grpc
import logging

from typing import Dict

import chatPrivat_pb2
import chatPrivat_pb2_grpc

from servei_chat import ServeiChat


# Dades dels clients dels chats: identificador i indicador de si està o no en línia
class ChatClient:
    id_client: int
    online: bool = True

    def __init__(self, id_client, online=True):
        self.id_client = id_client
        self.online = online

    def is_online(self) -> bool:
        return self.online

    def set_online(self, online) -> None:
        self.online = online


# Servidor
class Server(chatPrivat_pb2_grpc.PrivateChatsServiceServicer):
    # Serveis d'escriptura i lectura de missatges
    servei_chat: ServeiChat = ServeiChat()
    # Diccionari per emmagatzemar els clients
    clients: Dict[int, ChatClient] = {}

    async def EnviarMissatge(self, request: chatPrivat_pb2.PeticioMissatge, context: grpc.aio.ServicerContext) -> chatPrivat_pb2.RespostaMissatge:
        try:
            logging.info(f"EnviarMissatge amb el paràmetre {request=}")
            # El client ha demanat tancar la connexió
            if request.missatge == "EXIT":
                logging.info(f"Remitent={request.id_remitent} desconnectant-se.")
                if request.id_remitent in self.clients.keys():
                    # Modifiquem l'estat del client
                    self.clients[request.id_remitent].set_online(False)
                # L'id del destinatari passa a ser el del remitent que ha demanat desconnectar-se
                request.id_destinatari = request.id_remitent
            await self.servei_chat.escriure_missatge(request)
        except asyncio.CancelledError:
            print("Cancelled")
            raise
        return chatPrivat_pb2.RespostaMissatge()

    async def RebreMissatges(self, request: chatPrivat_pb2.Client, context: grpc.aio.ServicerContext) -> chatPrivat_pb2.Missatge:
            logging.info(f"RebreMissatges amb el paràmetre {request=}")
            # Comprovar que tenim el client que ha de rebre els missatges
            # En cas que no, afegir-lo
            if not self.clients.get(request.id_destinatari):
                self.clients[request.id_destinatari] = ChatClient(request.id_destinatari, True)
            else:
                # Indicar com a connectat al client destinatari dels missatges
                self.clients[request.id_destinatari].online = True
            while self.__client_connectat(request.id_destinatari):
                missatge = await self.servei_chat.llegir_missatge(request)
                # Per tal de desconnectar-se
                if missatge.missatge == "EXIT":
                    break
                yield missatge

    # Consultar si el client està o no connectat
    def __client_connectat(self, id_client):
        if id_client not in self.clients.keys():
            return False
        return self.clients[id_client].is_online()


async def serve() -> None:
    server = grpc.aio.server()
    chatPrivat_pb2_grpc.add_PrivateChatsServiceServicer_to_server(Server(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info(f"Iniciant servidor a {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    except KeyboardInterrupt:
        print("Tancant servidor...")
    finally:
        loop.close()
