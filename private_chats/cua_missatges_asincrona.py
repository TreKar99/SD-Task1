import logging
from asyncio import Queue
from typing import Dict


class CuaMissatgesAsincrona:

    topics: Dict[int, Queue] = {}

    # Obtenir el nombre de missatges que hi ha a la cua
    def get_nombre_missatges(self, id_destinatari):
        cua_destinatari = self.__get_or_create_queue(id_destinatari)
        return cua_destinatari.qsize()

    # Afegir un missatge a la cua del destinatari
    async def put_missatge(self, id_destinatari, missatge):
        # Obtenir la cua del destinatari, en cas que no existeixi, es crea
        cua_destinatari = self.__get_or_create_queue(id_destinatari)
        # Obtenir el identificador del missatge que afegirem
        id_missatge = cua_destinatari.qsize()
        await cua_destinatari.put(missatge)
        logging.info(f"Missatge afegit a la cua del destinatari={id_destinatari}")
        # Retornar l'identificador del missatge afegit a la cua
        return id_missatge

    # Obtenir un missatge de la cua del destinatari
    async def get_missatge(self, id_destinatari):
        # Obtenir la cua del destinatari, en cas que no existeixi, es crea
        cua_destinatari = self.__get_or_create_queue(id_destinatari)
        logging.info(f"Llegint de la cua pel destinatari={id_destinatari}")
        # Obtenir el missatge de la cua
        nou_missatge = await cua_destinatari.get()
        logging.info(f"Nou missatge rebut pel destinatari={id_destinatari}")
        return nou_missatge

    # Obtenir la cua del destinatari amb l'id indicat per paràmetre
    # En cas de no existir la cua, aquesta es crea
    def __get_or_create_queue(self, id_destinatari):
        if not self.topics.get(id_destinatari):
            self.topics[id_destinatari] = Queue()
        return self.topics[id_destinatari]
