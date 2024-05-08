import chatPrivat_pb2
import cua_missatges_asincrona


class ServeiChat:
    cua_missatges = cua_missatges_asincrona.CuaMissatgesAsincrona = cua_missatges_asincrona.CuaMissatgesAsincrona()

    # Inserir els missatges rebuts al topic del destinatari
    async def escriure_missatge(self, peticio: chatPrivat_pb2.PeticioMissatge) -> chatPrivat_pb2.RespostaMissatge:
        id_destinatari = peticio.id_destinatari
        # L'id del pròxim missatge serà el nombre de missatges que hi ha a la cua actualment
        id_missatge = self.cua_missatges.get_nombre_missatges(id_destinatari)
        # Inserir a la cua del destinatari el missatge (creant un objecte Missatge amb les dades del missatge a enviar)
        id_missatge = await self.cua_missatges.put_missatge(
            id_destinatari=peticio.id_destinatari,
            missatge=chatPrivat_pb2.Missatge(
                id=id_missatge, id_thread=peticio.id_thread,
                missatge=peticio.missatge, id_remitent=peticio.id_remitent,
                id_destinatari=id_destinatari,
            ),
        )
        return chatPrivat_pb2.RespostaMissatge(id=id_missatge)

    # Llegir un missatge del topic per enviar-li al destinatari
    async def llegir_missatge(self, peticio: chatPrivat_pb2.Client) -> chatPrivat_pb2.Missatge:
        return await self.cua_missatges.get_missatge(peticio.id_destinatari)
