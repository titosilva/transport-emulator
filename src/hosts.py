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
        packet = None
        # Verifica se foram recebidos pacotes e faz o processamento
        while True:
            try:
                packet = self.__recvpackets.popleft()
                
            except:
                break

        # Envia pacotes
        


class ReceiverGBN(PacketHandler):
    pass

