from packet_handler import *
from connection import *
import time

# Emissor Go-Back-N
class EmitterGBN(HostType):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca o construtor da classe base
        super().__init__(srcid, destid)

        # Base para a contagem dos pacotes enviados
        self.__base = 1
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

        # Quantidade total de bytes ja enviados
        self.__senttotal = 0


    def getSequenceNumber(self):
        return self.__seq

    def getSentTotal(self):
        return self.__senttotal

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setEmitter(self)

    def setWindowSize(self, winsz: int)->bool:
        if winsz>0:
            self.__winsz = winsz
            return True
        else:
            return False

    def setTimeout(self, timeout: float):
        self.__timeout = timeout
    
    # Funções que controlam o temporizador
    def __startTimer(self):
        self.__timer = time.time()

    def __getTime(self): 
        return time.time() - self.__timer

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
            data = bytes(b'This is a test packet')

            # Gera novo pacote
            packet = TCPSegment()
            packet.setData(data)

            # Adiciona pacote ao final da fila de pacotes a serem enviados
            self.add_to_send_packet(packet)

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

               # Adiciona o tamanho do pacote, em bytes, à contagem da quantidade total de bytes enviados
                self.__senttotal += packet.getSize()

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
        

# Receptor Go-Back-N
class ReceiverGBN(HostType):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca construtor da classe base
        super().__init__(srcid, destid)

        # Numero de sequencia esperado
        self.__seq = 1

        # Quantidade total de bytes ja enviados
        self.__senttotal = 0

        # Pacote para reconhecimentos
        self.__sndpkt = ACK(acknum=self.__seq)

        # Conexão
        self.setConnection(connection)

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setReceiver(self)

    def getExpectedSequenceNumber(self):
        return self.__seq

    def getSentTotal(self):
        return self.__senttotal

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
                    self.__sndpkt = ACK(acknum=self.__seq)
                    self.add_to_send_packet(self.__sndpkt)
                    self.__seq += 1
                else:
                    # Se nao for o numero de sequencia esperado, apenas reenviada ACK com ultimo numero
                    # de sequencia recebido corretamente
                    self.add_to_send_packet(self.__sndpkt)
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

                # Adiciona o tamanho do pacote, em bytes, à contagem da quantidade total de bytes enviados
                self.__senttotal += packet.getSize()
            except:
                # Quando nao ha mais pacotes, é lançada uma excessão e o while é finalizado
                break

    def run(self):
        self.__analyseReceivedPackets()
        self.__sendPackets()


# Emissor Stop-and-Wait
class EmitterSW(HostType):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca o construtor da classe base
        super().__init__(srcid, destid)

        # Controle da sequencia (0 e 1)
        self.__seq = 1
        # Quantidade total de bytes ja enviados
        self.__senttotal = 0
        # Quantidade de pacotes ja enviados e confirmados
        self.__ackedtotal = 0
        # Indica se há pacotes sendo esperados para serem recebidos
        self.__wait = False
        # Timeout (tempo maximo ate o reenvio)
        self.__timeout = 0
        # Time (tempo passado desde a ultima chamada de StartTimer)
        self.__timer = time.time()
        # Conexão
        self.setConnection(connection)

    def getSequenceNumber(self):
        return self.__seq

    def getSentTotal(self):
        return self.__senttotal

    def getAckedTotal(self):
        return self.__ackedtotal

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setEmitter(self)

    def setTimeout(self, timeout: float):
        self.__timeout = timeout
    
    # Funções que controlam o temporizador
    def __startTimer(self):
        self.__timer = time.time()

    def __getTime(self): 
        return time.time() - self.__timer

    def __stopTimer(self):
        self.__timer = time.time()

    def __analyseReceivedPacket(self):
        # Verifica se foi recebido um ACK e faz seu processamento
        try:
            # Pega um pacote do buffer de recebimento (o buffer contem tuples, entao pegamos o primeiro elemento
            # da tuple, que corresponde, na implementação, ao pacote)
            packet = self._recvpackets.popleft()[0]

            # Como é esperado apenas o recebimento de um pacote, esvaziamos o buffer para o caso 
            # no qual outros pacotes que não deviam ser recebidos tenham sido recebidos
            self._recvpackets.clear()

            # Verifica se o pacote é um ACK
            if packet.isACK():
                # Verifica o numero de ACK (0 ou 1)
                ack = packet.getAckNumber()

                # Se o ACK recebido é o esperado, desativamos o temporizador de timeout
                # e removemos o pacote ja confirmado para que possa ser enviado o proximo pacote
                if ack == self.__seq:
                    try: 
                        self.__sendpackets.clear()
                    except:
                        pass
                    self.__wait = False
                    # Trocamos o numero de sequencia, de 0 para 1 ou vice-versa
                    self.__seq = (self.__seq+1)%2
                    self.__stopTimer()
                    # Adicionamos à contagem de pacotes reconhecidos
                    self.__ackedtotal += 1
                else:
                    # Caso não seja recebido ack esperado,
                    # Reenviamos o pacote. Para isso, somente precisamos esperar
                    # o timeout
                    pass
        except:
            # Se não há pacotes, apenas finaliza a execução da função
            return

    # Gera um pacote para ser enviado, caso nao hajam pacotes a serem enviados
    def __genPacket(self):
        if len(self._sendpackets)==0:
            # Dados em bytes para teste
            data = bytes(b'This is a test packet')

            # Gera novo pacote
            packet = TCPSegment()
            packet.setData(data)

            # Guarda pacote para ser enviado posteriormente
            self.add_to_send_packet(packet)

    def __verifyTimeout(self)->bool:
        # Verifica se o timeout foi alcançado
        if self.__getTime() >= self.__timeout:
            # Se o timeout for alcançado, os pacote deve ser reenviado  
            self.__sendPacket()
            # Caso seja reenviado o pacote, é retornado True, indicando
            # a ocorrencia
            return True
        else:
            return False

    def __sendPacket(self):
        # entrega o pacote à conexão
        # inicia o timer para timeout
        self.__startTimer()
        self.__wait = True

        # Pega pacote do buffer de pacotes
        packet = self.get_to_send_packet(0)

        if packet != None:        
            # Coloca o numero de sequencia no pacote
            packet.setSequenceNumber(self.__seq)

            # Envia o pacote
            self.__connection.receive_packet(packet, self._srcid, self._destid)

            # Adiciona o tamanho do pacote, em bytes, à contagem da quantidade total de bytes enviados
            self.__senttotal += packet.getSize()

    def run(self):
        # Verifica o pacote recebido
        self.__analyseReceivedPacket()

        # Gera um pacote a ser enviado, caso o ultimo pacote ja tenha sido confirmado
        self.__genPacket()

        # Verifica o timeout, se ainda houverem pacotes a serem recebidos
        if self.__wait:
            # Se o timeout for atingido, envia os pacotes e para a execução da função
            if self.__verifyTimeout():
                return
        else:
            # Caso nao sejam esperado pacote de confirmação, envia novo pacote
            self.__sendPacket()


# Receptor SW
class ReceiverSW(HostType):
    def __init__(self, srcid: str, destid: str, connection: SimpleConnection):
        # Invoca construtor da classe base
        super().__init__(srcid, destid)

        # Numero de sequencia esperado
        self.__seq = 1

        # Quantidade total de bytes ja enviados
        self.__senttotal = 0


        # Pacote para reconhecimentos
        self.__sndpkt = ACK(acknum=self.__seq)

        # Conexão
        self.setConnection(connection)

    def getExpectedSequenceNumber(self):
        return self.__seq

    def getSentTotal(self):
        return self.__senttotal

    # Define a conexão por onde serão enviados os pacotes
    def setConnection(self, connection: SimpleConnection):
        self.__connection = connection
        self.__connection.setReceiver(self)


    # Analisa os pacotes recebidos
    def __analyseReceivedPacket(self):
            try:
                # Tentamos retirar um pacote da fila de pacotes recebidos
                packet = self._recvpackets.popleft()[0]

                # Limpamos o buffer para o caso de serem recebidos outros pacotes, o que nao e esperado
                try:
                    self._recvpackets.clear()
                except:
                    pass
                
                # Verifica se o numero de sequencia do pacote é o esperado
                if packet.getSequenceNumber() == self.__seq:
                    # Se for, adiciona ACK à fila de pacotes a serem enviados 
                    # e muda o numero de sequencia esperado
                    self.__sndpkt = ACK(acknum=self.__seq)
                    self.add_to_send_packet(self.__sndpkt)
                    self.__seq = (self.__seq + 1)%2
                else:
                    # Se nao for o numero de sequencia esperado, apenas reenvia ACK com ultimo numero
                    # de sequencia recebido corretamente
                    self.add_to_send_packet(self.__sndpkt)
            except:
                # Quando não há mais pacotes, é lançada uma excessão e a execução da funçao é finalizada
                return

    # Função usada para enviar ACK's
    def __sendPacket(self):
        try:
            # Pega o pacote da fila de pacotes a serem enviados
            packet = self._sendpackets.popleft()
            
            # Entrega o pacote a conexão
            self.__connection.receive_packet(packet, self._srcid, self._destid)

            # Adiciona o tamanho do pacote, em bytes, à contagem da quantidade total de bytes enviados
            self.__senttotal += packet.getSize()
        except:
            return

    def run(self):
        self.__analyseReceivedPacket()
        self.__sendPacket()
