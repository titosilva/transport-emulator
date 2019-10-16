from collections import deque
import abc

class Packet(object):
    def __init__(self, data: bytes):
        self.__data = data

    def setData(self, data: bytes):
        self.__data = data

    def getData(self, data: bytes)->bytes:
        return self.__data

class PacketHandler(metaclass=ABCMeta):
    def __init__(self):
        self.__packets = deque()
    
    @abc.abstractmethod
    def run(self):
        pass

    def recv_packet(self, p: Packet):
        self.__packets.append(p)
    
    def send_packet(self, p:Packet):
        self.__packets.popleft()

    def getPackets(self)->deque:
        return self.__packets
