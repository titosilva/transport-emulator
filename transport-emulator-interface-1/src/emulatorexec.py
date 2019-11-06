from hosts import *
from connection import *
import time

# Usando padrão singleton para garantir que haja apenas uma instância de simulador

# Emulador de protocolo GBN
class EmulatorGBN(object):
    class __EmulatorGBN:
        def __init__(self, emitterid: str, receiverid: str):
            self.connection = SimpleConnection()
            self.emitter = EmitterGBN(emitterid, receiverid, self.connection)
            self.receiver = ReceiverGBN(receiverid, emitterid, self.connection)

    # Instancia de emulador
    __emul = None

    # Identificadores de emissor e receptor
    __emitterid = 'e'
    __receiverid = 'r'

    def __init__(self):
        # Cria a instancia, caso nao exista 
        if not EmulatorGBN.__emul:
            EmulatorGBN.__emul = EmulatorGBN.__EmulatorGBN(EmulatorGBN.__emitterid, EmulatorGBN.__receiverid)
        # Reseta a instancia, caso exista
        else:   
            EmulatorGBN.__emul = None
            EmulatorGBN.__emul = EmulatorGBN.__EmulatorGBN(EmulatorGBN.__emitterid, EmulatorGBN.__receiverid) 

    def setEmitterParams(self, winsz: int, timeout: float):
        if not EmulatorGBN.__emul.emitter.setWindowSize(winsz):
            raise Exception

        EmulatorGBN.__emul.emitter.setTimeout(timeout)

    def setConnectionParams(self, loss: int, rate: float, distance: float, speed: float):
        if not  EmulatorGBN.__emul.connection.setLoss(loss):
            raise Exception

        EmulatorGBN.__emul.connection.setRate(rate)
        EmulatorGBN.__emul.connection.setDistance(distance)
        EmulatorGBN.__emul.connection.setSpeed(speed)

    def printState(self):
        print('\npackets on connection' + '\t' + str(time.time()))
        for packet in self.__emul.connection.getPackets()[0]:
            print(str(packet[0].getSequenceNumber()) + '\t' + str(packet[0].getAckNumber()) +'\t' +  packet[1] + '\t' +  packet[2] + '\t' + str(packet[0].isACK()) + '\t' + str(packet[0].getData()))

    def run(self):
        self.__emul.emitter.run()
        self.__emul.connection.run()
        self.__emul.receiver.run()

# Emulador de protocolo Stop-and-wait
class EmulatorSW(object):
    class __EmulatorSW:
        def __init__(self, emitterid: str, receiverid: str):
            self.connection = SimpleConnection()
            self.emitter = EmitterSW(emitterid, receiverid, self.connection)
            self.receiver = ReceiverSW(receiverid, emitterid, self.connection)

    # Instancia de emulador
    __emul = None

    # Identificadores de emissor e receptor
    __emitterid = 'e'
    __receiverid = 'r'

    def __init__(self):
        # Cria a instancia, caso nao exista 
        if not EmulatorSW.__emul:
            EmulatorSW.__emul = EmulatorSW.__EmulatorSW(EmulatorSW.__emitterid, EmulatorSW.__receiverid)
        # Reseta a instancia, caso exista
        else:   
            EmulatorSW.__emul = None
            EmulatorSW.__emul = EmulatorSW.__EmulatorSW(EmulatorSW.__emitterid, EmulatorSW.__receiverid) 

    def setEmitterParams(self, timeout: float):
        EmulatorSW.__emul.emitter.setTimeout(timeout)

    def setConnectionParams(self, loss: int, rate: float, distance: float, speed: float):
        if not  EmulatorSW.__emul.connection.setLoss(loss):
            raise Exception

        EmulatorSW.__emul.connection.setRate(rate)
        EmulatorSW.__emul.connection.setDistance(distance)
        EmulatorSW.__emul.connection.setSpeed(speed)

    def printState(self):
        print('\npackets on connection' + '\t' + str(time.time()))
        for packet in self.__emul.connection.getPackets()[0]:
            print(str(packet[0].getSequenceNumber()) + '\t' + str(packet[0].getAckNumber()) +'\t' +  packet[1] + '\t' +  packet[2] + '\t' + str(packet[0].isACK()) + '\t' + str(packet[0].getData()))

    def run(self):
        self.__emul.emitter.run()
        self.printState()
        self.__emul.connection.run()
        self.printState()
        self.__emul.receiver.run()
