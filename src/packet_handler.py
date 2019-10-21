from collections import deque
from packet_struct import *
import abc

class PacketHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__packets = deque()
    
    @abc.abstractmethod
    def run(self):
        pass

    def append_packet(self, p: Packet):
        self.__packets.append(p)
    
    def pop_packet(self, p:Packet)->bool:
        packet = None

        try:
            packet = self.__packets.popleft()
        except:
            return False

        return True
        

    def getPackets(self)->deque:
        return self.__packets
