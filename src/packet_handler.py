from collections import deque
from packet_struct import *
import abc

class PacketHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        # Destino dos pacotes que serão enviados
        self.__recvpackets = deque()
    
    @abc.abstractmethod
    def run(self):
        pass

    def receive_packet(self, p: Packet):
        self.__recvpackets.append(p)

    def getPackets(self)->(deque, deque):
        return (self.__recvpackets, self.__sendpackets)
