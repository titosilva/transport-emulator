from packet_handler import *
from collections import *
import time
import random

class SimpleConnection(PacketHandler):
    def __init__(self, receiver: HostType = None, emitter: HostType = None, recvid: str = None, emitterid: str = None, distance: float=0, rate: float=1.0, loss: int=100, speed: float=1.0):
        super().__init__()
        self.setEmitter(emitter)
        self.setReceiver(receiver)
        self.__distance = distance
        self.__speed = speed
        self.__rate = rate
        self.__loss = loss
        self.__times = deque()
        self.__delay = 0

    def setReceiver(self, receiver: HostType):
        self.__receiver = receiver

    def setEmitter(self, emitter: HostType):
        self.__emitter = emitter

    # Metodo privado que calcula, a partir dos atributos, qual será o atraso
    def __calculateDelay(self):
        self.__delay = (self._recvpackets[0][0].getSize()/self.__rate) + (self.__distance/self.__speed)
        return self.__delay

    def setDistance(self, distance: float):
        self.__distance = distance

    def setSpeed(self, speed: float):
        self.__speed = speed

    def setRate(self, rate: float):
        self.__rate = rate

    def setLoss(self, loss: int)->bool:
        if 0<=loss and loss<=100:
            self.__loss = loss
            return True
        else:
            return False

    def receive_packet(self, p: Packet, srcid: str, destid: str):
        # Sobrecarregamos a função receive_packet com a intenção de associar, dentro
        # da conexão, cada pacote recebido ao tempo em que foi recebido
        # Para resolver esse problema, construimos um deque que cresce em paralelo com
        # o deque recv_packets, e contem, em cada posição, o tempo em que o pacote de
        # de mesma posição no deque recv_packets foi recebido.

        # Invoca metodo receive_packet da classe base
        super(SimpleConnection, self).receive_packet(p, srcid, destid)
        # Adiciona o tempo em que o pacote foi recebido à fila
        self.__times.append(time.time())

    def run(self):
        # Verifica se o tempo de enviar um pacote é chegado
        # O tempo self.__times[0] indica o tempo do pacote mais antigo
        # no buffer de pacotes recebidos
        while len(self._recvpackets)>0:
            self.__calculateDelay()
            if time.time() - self.__times[0] >= self.__delay:
                # Obtem uma tuple com as informaçoes sobre o pacote
                # A partir do buffer de pacotes recebidos
                info = self._recvpackets.popleft()

                # Remove o tempo desse pacote da fila de tempos, uma 
                # vez que esse pacote ou sera perdido ou sera enviado
                self.__times.popleft()

                # Usa um random para determinar se o pacote sera enviado (simular perda de pacotes com probabilidade loss%)
                if random.randint(0,100) >= self.__loss:
                    # Verifica quem é o destinatario do pacote e o entrega
                    if info[2] == self.__receiver.getID():
                        self.__receiver.receive_packet(info[0], info[1], info[2])
                    elif info[2] == self.__emitter.getID():
                        self.__emitter.receive_packet(info[0], info[1], info[2])
                    else:
                        # Se o destinatario é desconhecido, descarta o pacote
                        pass
                else:
                    # Caso o numero gerado seja menor que loss,
                    # apenas descarta o pacote
                    print('lost:' + str(info[0].getSequenceNumber()))
                    pass
            else:
                break



