from packet_handler import *
from connection import *
import time

class EmitterGBN(HostType):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca o construtor da classe base
        super().__init__(srcid, destid)

        # Base para a contagem dos pacotes enviados
        self.__base = 0
        # Numero de sequencia e numero de reconhecimento
        self.__ack = 0
        self.__seq = self.__base
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

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setEmitter(self)

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

    def __analyseReceivedPackets(self):
        # Verifica se foram recebidos pacotes e faz o processamento de cada um deles
        while True:
            try:
                # Pega um pacote do buffer de recebimento
                packet = self._recvpackets.popleft()[0]

                # Verifica se o pacote é um ACK
                if packet.isACK():
                    # Verifica o numero de ACK
                    ack = packet.getAckNumber() + 1

                    # Remove os pacotes ja confirmados do buffer de envio
                    for i in range(ack - self.__base):
                        self._sendpackets.popleft()

                    # Atualiza a base
                    self.__base = ack

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

    # Gera "quant" pacotes para serem enviados
    def __genPackets(self, quant: int):
        for i in range(quant):
            # Dados em bytes para teste
            data = bytes('This is a test packet')

            # Gera novo pacote
            packet = TCPSegment()
            packet.setData(data)

            # Adiciona pacote ao final da fila de pacotes a serem enviados
            self.add_packet_to_send(packet)

    def __verifyTimeout(self)->bool:
        # Verifica se o timeout foi alcançado
        if self.__getTime() >= self.__timeout:
            # Se o timeout for alcançado, os pacotes devem ser reenviados
            self.__sendPackets()
            # Caso sejam reenviados os pacotes, é retornado True, indicando
            # a ocorrencia
            return True
        else:
            return False

    def __sendPackets(self):
        # Tenta enviar pacotes para a conexão
        # Verifica se foram enviados todos os pacotes dentro da janela
        self.__seq = self.__base
        while self.__seq != self.__base + self.__winsz:
            # Inicia o timer antes de enviar o primeiro pacote
            if self.__seq == self.__base:
                self.__startTimer()

            # Pega pacote do buffer de pacotes a serem enviados
            # O pacote a ser pego estara na posição seq - base
            packet = self.get_to_send_packet(self.__seq - self.__base)

            # Coloca o numero de sequencia no pacote
            packet.setSequenceNumber(self.__seq)

            # Envia o pacote
            if packet != None:
                # Entrega pacotes à conexão, que, por sua vez, os entregará ao destinatário(receiver)
                self.__connection.receive_packet(packet, self._srcid, self._destid)

                # Incrementa o numero de sequencia
                self.__seq += 1

                # Coloca wait em True, indicando que há ACK's a serem recebidos
                self.__wait = True
            else:
                # Caso seja recebido um pacote None, nao há mais pacotes a serem enviados
                break

    def run(self):
        # Verifica os pacotes recebidos
        self.__analyseReceivedPackets()

        # Gera pacotes a serem enviados (equivalente ao rdt_send)
        # Por simplicidade, a cada ciclo, será gerada uma quantidade de pacotes
        # Igual ao restante da janela que ainda esta disponivel
        self.__genPackets(self.__winsz - len(self._sendpackets))

         # Verifica o timeout, se ainda houverem pacotes a serem recebidos
        if self.__wait:
            # Se o timeout for atingido, envia os pacotes e para a execução da função
            if self.__verifyTimeout():
                return
        else:
            # Caso nao sejam esperados pacotes,
            # envia os novos pacotes
            self.__sendPackets()
        


class ReceiverGBN(PacketHandler):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca construtor da classe base
        super().__init__()

        # Numero de sequencia esperado
        self.__seq = 0

        # Conexão
        self.setConnection(connection)
        # ID da fonte
        self.setID(srcid)
        # ID do destino
        self.setDestID(destid)

    def setID(self, idstr: str):
        self._srcid = idstr

    def setDestID(self, idstr: str):
        self._destid = idstr

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setReceiver(self)


    # Analisa os pacotes recebidos
    def __analyseReceivedPackets(self):
        while True:
            try:
                # Tentamos retirar um pacote da fila de pacotes recebidos
                packet = self._recvpackets.popleft()[0]
                
                # Verifica se o numero de sequencia do pacote é o esperado
                if packet.getSequenceNumber() == self.__seq:
                    # Se for, adiciona ACK à fila de pacotes a serem enviados 
                    # e incrementa o numero de sequencia esperado
                    self.add_to_send_packet(ACK(acknum=self.__seq))
                    self.__seq += 1
                else:
                    # Se nao for o numero de sequencia esperado, apenas reenviada ACK com ultimo numero
                    # de sequencia recebido corretamente
                    self.add_to_send_packet(ACK(acknum=self.__seq))
            except:
                # Quando não há mais pacotes, é lançada uma excessão e a execução do while é finalizada
                break

    # Função usada para enviar ACK's
    def __sendPackets(self):
        while True:
            try:
                # Pega um pacote da fila de pacotes a serem enviados
                packet = self._sendpackets.popleft()
                
                # Entrega o pacote a conexão
                self.__connection.receive_packet(packet, self._srcid, self._destid)
            except:
                # Quando nao ha mais pacotes, é lançada uma excessão e o while é finalizado
                break

    def run(self):
        self.__analyseReceivedPackets()
        self.__sendPackets()
