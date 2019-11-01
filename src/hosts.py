from packet_handler import *
from connection import *
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
        # Lista que armazena os pacotes que podem ser reenviados
        self.__resend = []

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

    def __verifyTimeout(self):
        # Verifica se o timeout foi alcançado
        if self.__getTime() >= self.__timeout:
            # Se o timeout for alcançado, os pacotes devem ser reenviados
            pass

    def __analyseReceivedPackets(self):
        # Verifica se foram recebidos pacotes e faz o processamento de cada um deles
        while True:
            try:
                # Pega um pacote do buffer de recebimento
                packet = self.__recvpackets.popleft()
                # Verifica se o pacote é um ACK
                if packet.isACK():
                    # Verifica o numero de ACK
                    self.__base = packet.getAckNumber() + 1
                    # Se a base é igual ao proximo numero de sequencia, todos os pacotes foram recebidos
                    if self.__base == self.__seq:
                        self.__wait = False
                        self.__stopTimer()
                    else:
                        # Caso não seja recebido ack para os pacotes de toda a janela, 
                        # reinicia o temporizador
                        self.__startTimer()
            except:
                # Quando não há mais pacotes, é lançada uma excessão e a execução do while é finalizada
                break

    def __rdt_send(self):
        pass

    def __sendPackets(self):
        # Tenta enviar pacotes para a conexão
        while True:
            # Pega pacote do buffer de pacotes a serem enviados
            packet = self.get_to_send_packet()
            packet.setSequenceNumber(self.__seq)
            # Inicia o timer
            self.__startTimer()
            self.__wait = True
            if packet != None:
                # Adiciona o pacote à lista de pacotes que podem ser reenviados
                self.__resend.append(packet)

                # Entrega pacotes à conexão
                self.__connection.receive_packet(packet, self.__srcid, self.__destid)

                # Incrementa o numero de sequencia
                self.__seq += 1
            else:
                break

    def run(self):
        # Verifica o timeout, se ainda houverem pacotes a serem recebidos
        if self.__wait:
            self.__verifyTimeout()

        # Verifica os pacotes recebidos
        self.__analyseReceivedPackets()

        # Gera pacotes a serem enviados (equivalente ao rdt_send)
        self.__rdt_send()

        # Envia os pacotes que foram gerados
        self.__sendPackets()
        


class ReceiverGBN(PacketHandler):
    pass

