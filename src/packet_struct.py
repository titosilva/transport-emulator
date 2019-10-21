import abc

class Packet(metaclass=abc.ABCMeta):
    __data = None

    @abc.abstractmethod
    def getSize(self)->int:
        pass

    def setData(self, data: bytearray):
        self.__data = data

    def getData(self)->bytes:
        return self.__data

class TCPSegment(Packet):
    def setSourcePort(self, srcprt: int)->bool:
        if 0 <= srcprt <= 65535:
            self.__srcprt = srcprt
            return True
        return False

    def setDestinationPort(self, dstprt: int)->bool:
        if 0 <= dstprt <= 65535:
            self.__dstprt = dstprt
            return True
        return False

    def setSequenceNumber(self, seqnum: int):
        self.__seqnum = seqnum

    def setAcknowledgementNumber(self, acknum: int):
        self.__acknum = acknum

    def setHeaderSize(self, headersz: int):
        if 5 <= headersz <= 15:
            self.__headsz = headersz
            return True
        return False

    def setWindowSize(self, winsz: int):
        if 0 <= winsz <= 65535:
            self.__winsz = winsz
            return True
        return False

    def setChecksum(self, chsum: int):
        if 0 <= chsum <= 65535:
            self.__chsum = chsum
            return True
        return False

    def setUrgentPointer(self, urgpnt: int):
        if 0 <= urgpnt <= 65535:
            self.__urgpnt = urgpnt
            return True
        return False

    def setOptions(self, options: bytearray):
        if len(options) <= 5:
            self.__options = options
            self.setHeaderSize(5 + len(options)*2)
            return True
        return False
        

    def setFlags(self, urg: bool=False, ack: bool=False, psh: bool=False, rst: bool=False, syn: bool=False, fin: bool=False):
        self.__urg = urg
        self.__ack = ack
        self.__psh = psh
        self.__rst = rst
        self.__syn = syn
        self.__fin = fin
    
    # Todas as flags são colocadas como False inicialmente
    def __init__(self, srcprt: int=0, dstprt: int=0, seqnum: int=0, acknum: int=0, headersz: int=0, winsz: int=0, chsum: int=0, urgpnt: int=0, opt: bytearray = bytearray(0)):
        # Source port
        if not self.setSourcePort(srcprt):
            raise ValueError
        # Destination port
        if not self.setDestinationPort(dstprt):
            raise ValueError
        # Sequence number
        if not self.setSequenceNumber(seqnum):
            raise ValueError
        # Acknowledgement Number
        if not self.setAcknowledgementNumber(acknum):
            raise ValueError
        # Header Size
        if not self.setHeaderSize(headersz):
            raise ValueError
        # Set all flags to false
        self.setFlags()
        # Window Size
        if not self.setWindowSize(winsz):
            raise ValueError
        # Checksum
        if not self.setChecksum(chsum):
            raise ValueError
        # Urgent pointer
        if not self.setUrgentPointer(urgpnt):
            raise ValueError
        # Options
        if not self.setOptions(opt):
            raise ValueError

    # Retorna o tamanho do pacote em bytes
    def getSize(self):
        return len(self.__data) + self.__headsz/2