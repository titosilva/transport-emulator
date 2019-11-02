from packet_handler import *
from collections import *
import time
import random

class SimpleConnection(PacketHandler):
    def __init__(self, receiver: PacketHandler = None, emitter: PacketHandler = None, recvid: str = None,
                 emitterid: str = None, distance, rate, loss, speed):
        self.__emitter = emitter
        self.__receiver = receiver
        self.__distance = distance
        self.__speed = speed
        self.__rate = rate
        self.__loss = loss
        self.__times = deque()
        pass

    def receive_packet(self,packet, __srcid, __destid):
        super(SimpleConnection, self).receive_packet(self,packet, __srcid, __destid)
        self.__times.append(time.time())

    def run(self):
        if (self.times() - self.__times[0] >= (self._recvpackets[0].getSize()/self.rate)+(self.distance/self.speed)):
            if(random([0,100]) >= self.loss):
                self.ReceiverGBN.receive_packet(self._recvpackets[0], self.__srcid, self.__destid)
            else:
                return



