from packet_handler import *
from network import *
import time

class EmitterGBN(PacketHandler):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Base para a contagem dos pacotes enviados
        self.__base = 0
        # Numero de sequencia e numero de reconhecimento
        self.__ack = 0
        self.__seq = 0
        # Tamanho da janela
        self.__winsz = 0
        # Indica se há pacotes sendo esperados para serem recebidos
        self.__wait = False
        # Timeout (tempo maximo ate o reenvio)
        self.__timeout = 0
        # Time (tempo passado desde a ultima chamada de StartTimer)
        self.__timer = time.time()
        # Conexão
        self.setConnection(connection)
        # ID da fonte
        self.setID(srcid)
        # ID do destino
        self.setDestID(destid)

    def setID(self, idstr: str):
        self.__srcid = idstr

    def setDestID(self, idstr: str):
        self.__destid = idstr

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection

    def __setTimeout(self, timeout: float):
        self.__timeout = timeout
    
    # Funções que controlam o temporizador
    def __startTimer(self):
        self.__timer = time.time()

    def __getTime(self):
        self.__timer = time.time() - self.__timer
        return self.__timer

    def __stopTimer(self):
        self.__timer = time.time()

    def __sendPackets(self):
        # Tenta enviar pacotes para a conexão
        while True:
            packet = self.get_to_send_packet()
            if packet != None:
                self.__connection.receive_packet(packet, self.__srcid, self.__destid)
            else:
                break

    def __AnalyseReceivedPackets(self):
        # Verifica se foram recebidos pacotes e faz o processamento de cada um deles
        while True:
            try:
                packet = self.__recvpackets.popleft()
                if packet.isACK():
                    if packet.getAcknowledgeNumber() == self.__seq:
                        pass
            except:
                break

    def run(self):
        packet = None
        # Verifica se o timeout foi alcançado
        if self.__wait:
            if self.__getTime() >= self.__timeout:
                pass
        


class ReceiverGBN(PacketHandler):
    pass

