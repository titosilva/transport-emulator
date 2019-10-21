from packet_handler import *

class EmitterGBN(PacketHandler):
    def __init__(self):
        # Numero de sequencia e numero de reconhecimento
        self.__ack = 0
        self.__seq = 0
        # Tamanho da janela
        self.__winsz = 0
        # Timeout
        self.__timeout = 0

    def run(self):
        pass

class ReceiverGBN(PacketHandler):
    pass

