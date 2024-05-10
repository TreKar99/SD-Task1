import asyncio
import grpc
import logging
import cua_missatges_asincrona

import chatPrivat_pb2
import chatPrivat_pb2_grpc


# Servidor
class Server(chatPrivat_pb2_grpc.PrivateChatsServiceServicer):
    # Cua asíncrona que conté un diccionari amb la cua de cada client
    cua_missatges = cua_missatges_asincrona.CuaMissatgesAsincrona = cua_missatges_asincrona.CuaMissatgesAsincrona()

    # Funció asíncrona que envia els missatges a la cua del destinatari
    async def EnviarMissatge(self, peticio: chatPrivat_pb2.PeticioMissatge,
                             context: grpc.aio.ServicerContext) -> chatPrivat_pb2.RespostaMissatge:
        # Si el missatge que vol enviar el client correspon a "EXIT" aquest és una petició per tancar la connexió
        if peticio.missatge == "EXIT":
            logging.info(f"Client={peticio.id_remitent} desconnectant-se.")
            # L'id del destinatari passa a ser el del remitent que ha demanat desconnectar-se
            # D'aquesta manera, enviant-li l'EXIT li fem parar de llegir missatges
            peticio.id_destinatari = peticio.id_remitent

        # Inserir els missatges a la cua/topic del destinatari
        id_nou_missatge = self.cua_missatges.get_nombre_missatges(peticio.id_destinatari)
        # Inserir a la cua del destinatari el missatge (creant un objecte Missatge amb les dades del missatge a enviar)
        id_nou_missatge = await self.cua_missatges.put_missatge(
            id_destinatari=peticio.id_destinatari,
            missatge=chatPrivat_pb2.Missatge(
                id=id_nou_missatge, id_thread=peticio.id_thread,
                missatge=peticio.missatge, id_remitent=peticio.id_remitent,
                id_destinatari=peticio.id_destinatari,
            ),
        )
        return chatPrivat_pb2.RespostaMissatge(id=id_nou_missatge)

    # Funció asíncrona que obté els missatges rebuts a la cua del destinatari
    async def RebreMissatges(self, peticio: chatPrivat_pb2.Client,
                             context: grpc.aio.ServicerContext) -> chatPrivat_pb2.Missatge:
        # Comprovar que tenim el client que ha de rebre els missatges
        # En cas que no, afegir-lo

        # Estar rebent missatges fins desconnectar-se amb "EXIT"
        while True:
            missatge = await self.cua_missatges.get_missatge(peticio.id_destinatari)
            # Per tal de desconnectar-se
            if missatge.missatge == "EXIT":
                break
            yield missatge


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
