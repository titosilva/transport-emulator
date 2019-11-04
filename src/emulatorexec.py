from hosts import *
from connection import *

# Usando padrão singleton para garantir que haja apenas uma instância de simulador
class EmulatorGBN(object):
    class __EmulatorGBN:
        def __init__(self, emitterid: str, receiverid: str):
            self.connection = SimpleConnection()
            self.emitter = EmitterGBN(emitterid, receiverid, self.connection)
            self.receiver = ReceiverGBN(receiverid, emitterid, self.connection)

    # Instancia de emulador
    emul = None

    emitterid = 'd'
    receiverid = 'r'

    def __init__(self):
        # Cria a instancia, caso nao exista 
        if not EmulatorGBN.emul:
            EmulatorGBN.emul = EmulatorGBN.__EmulatorGBN(EmulatorGBN.emitterid, EmulatorGBN.receiverid)
        # Reseta a instancia, caso exista
        else:
            # EmulatorGBN.emul.connection = None
            # EmulatorGBN.emul.emitter = None
            # EmulatorGBN.emul.receiver = None

            # EmulatorGBN.emul.connection = SimpleConnection()
            # EmulatorGBN.emul.emitter = EmitterGBN(self.emitterid, receiverid, self.connection)
            # EmulatorGBN.emul.receiver = ReceiverGBN(receiverid, emitterid, self.connection)

            EmulatorGBN.emul = None
            EmulatorGBN.emul = EmulatorGBN.__EmulatorGBN(EmulatorGBN.emitterid, EmulatorGBN.receiverid)  


        

