from collections import deque
from packet_struct import *
import abc


# Classe base para todos o HostType e para SimpleConnection
class PacketHandler(metaclass=abc.ABCMeta):
    def __init__(self):
        # Pacotes recebidos
        self._recvpackets = deque()
        # Pacotes a serem enviados
        self._sendpackets = deque()
    
    # Metodo que define o modo como o PacketHandler que herdara dessa classe se comporta
    @abc.abstractmethod
    def run(self):
        pass

    # Adiciona um pacote a fila de pacotes a serem enviados
    # Caso o argumento left seja True, o pacote será adicionado
    # ao inicio da fila, ao inves do seu final
    # O retorno indica se foi possivel adicionar o pacote
    def add_to_send_packet(self, p: Packet, left: bool=False)->bool:
        try:
            if left:
                self._sendpackets.appendleft(p)
            else:
                self._sendpackets.append(p)

            return True
        except:
            return False

    # Retorna um pacote da fila de pacotes a serem enviados, sem removê-lo da fila
    # Deve ser dada a posição do pacote a ser retornado
    # Caso não hajam pacotes a serem enviados, é retornado None
    def get_to_send_packet(self, position: int)->Packet:
        try:
            packet = self._sendpackets[position]
            return packet
        except:
            return None

    # Metodo publico que permite a interação entre os hosts
    # Adiciona um pacote à fila de pacotes recebidos
    # Deve ser passado um ID da fonte, chamado srcid, o qual servira para identificar a fonte do pacote
    # Também deve ser passado um id de destinatario
    def receive_packet(self, p: Packet, srcid: str, destid: str):
        self._recvpackets.append((p, srcid, destid))

    # Retorna os buffers para visualização
    def getPackets(self)->(deque, deque):
        return (self._recvpackets, self._sendpackets)

# Classe base para todos os hosts
class HostType(PacketHandler):
    def __init__(self, srcid: str, destid: str):
        # Invoca metodo construtor da classe base
        super().__init__()
        # Define o id do host
        self.setID(srcid)
        # Define o id de quem é o destinatário dos pacotes
        self.setDestID(destid)

    def setID(self, idstr: str):
        self._srcid = idstr

    def getID(self)->str:
        return self._srcid

    def setDestID(self, idstr: str):
        self._destid = idstr
