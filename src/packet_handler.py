from collections import deque
from packet_struct import *
import abc

class PacketHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        # Pacotes recebidos
        self.__recvpackets = deque()
        # Pacotes a serem enviados
        self.__sendpackets = deque()
    
    @abc.abstractmethod
    def run(self):
        pass

    # Remove um pacote da fila de pacotes a serem enviados, e o retorna
    # Caso não hajam pacotes a serem enviados, é retornado None
    def get_to_send_packet(self)->Packet:
        try:
            packet = self.__sendpackets.popleft()
            return packet
        except:
            return None

    # Adiciona um pacote à fila de pacotes recebidos
    # Deve ser passado um ID da fonte, chamado srcid, o qual servira para identificar a fonte do pacote
    def receive_packet(self, p: Packet, srcid: str):
        self.__recvpackets.append((p,srcid))

    def getPackets(self)->(deque, deque):
        return (self.__recvpackets, self.__sendpackets)
