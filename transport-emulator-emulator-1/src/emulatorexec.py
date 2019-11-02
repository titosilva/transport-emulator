from hosts import *
from network import *

# Usando padrão singleton para garantir que haja apenas uma instância de simulador
class EmulatorGBN(object):
    class __EmulatorGBN:
        def __init__(self):
            self.emitter = EmitterGBN()
            self.receiver = ReceiverGBN()
            self.network = SimpleNetwork(self.rate,self.loss)

    # Instancia de emulador
    emul = None
    def __init__(self, rate: float=1.0):
        # Cria a instancia, caso nao exista
        if not EmulatorGBN.emul:
            EmulatorGBN.emul = EmulatorGBN.__EmulatorGBN()
        # Reseta a instancia, caso exista
        else:
            EmulatorGBN.emul.emitter = None
            EmulatorGBN.emul.receiver = None
            EmulatorGBN.emul.network = None

            EmulatorGBN.emul.emitter = EmitterGBN()
            EmulatorGBN.emul.receiver = ReceiverGBN()
            EmulatorGBN.emul.network = SimpleNetwork()

        self.__rate = rate

    def setRate(self, rate:float=1.0):
        self.__rate = rate


        

