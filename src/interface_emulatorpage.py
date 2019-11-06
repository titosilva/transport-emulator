import tkinter as tk
from emulatorexec import *

class EmulatorPage:
    # Usado para guardar o protocolo a ser simulado
    __mode = 'SW'
    # Usado para guardar referencia às labels de numero de sequencia
    __seqlabels = []
    # Usado para armazenar referencia às listbox
    __listboxes = []
    # Usado para controlar o loop de emulação (metodo run)
    __emulationstate = 0

    @staticmethod
    def setMode(mode: str):
        if mode == 'GBN' or mode == 'SW':
            EmulatorPage.__mode = mode
            return True
        else:
            EmulatorPage.__mode =  'GBN'
            return False

    @staticmethod
    def createEmulator():
        EmulatorPage.__emul = None
        if(EmulatorPage.__mode=='GBN'):
            EmulatorPage.__emul = EmulatorGBN()
        else:
            EmulatorPage.__emul = EmulatorSW()

    @staticmethod
    def setEmitterParams(winsz: int=10, timeout: float=10)->bool:
        try:
            EmulatorPage.__emul.setEmitterParams(winsz, timeout)
            return True
        except:
            return False

    @staticmethod
    def setConnectionParams(loss: int=0, rate: float=100000, distance: float=0, speed: float=10000)->bool:
        try:
            EmulatorPage.__emul.setConnectionParams(loss, rate, distance, speed)
            return True
        except:
            return False

    @staticmethod
    def run(delay: float, root: tk.Tk):
        # Executa os metodos run dos hosts e da connection no emulador
        # Mostra os pacotes na tela
        # Mostra os numeros de sequencia na tela
        state = None
        if EmulatorPage.__emulationstate == 0:
            EmulatorPage.__emul.runEmitter()
            state = EmulatorPage.__emul.getState()
            seq = EmulatorPage.__emul.getSequenceNumbers()
        elif EmulatorPage.__emulationstate == 1:
            EmulatorPage.__emul.runConnection()
            state = EmulatorPage.__emul.getState()
            seq = EmulatorPage.__emul.getSequenceNumbers()
        else:
            EmulatorPage.__emul.runReceiver()
            state = EmulatorPage.__emul.getState()
            seq = EmulatorPage.__emul.getSequenceNumbers()

        EmulatorPage.__emulationstate = (EmulatorPage.__emulationstate + 1)%3

        # Display packets in the listboxes
        for listbox in EmulatorPage.__listboxes:
            listbox.delete(0,'end')

        listcounter = 0
        pktcounter = 0
        for pktlist in state:
            for pkt in pktlist:
                EmulatorPage.__listboxes[listcounter].insert(pktcounter, pkt)
                pktcounter += 1
            listcounter += 1

        EmulatorPage.__seqlabels[0].config(text='Seq: '+str(seq[0]))
        EmulatorPage.__seqlabels[1].config(text='Seq: '+str(seq[1]))

        root.after(delay, lambda: EmulatorPage.run(delay, root))
                
    @staticmethod
    def emulate():    
        root = tk.Tk()
        root.title("Welcome to Shiba Emulator :)")

        modelabel = tk.Label(root, text='Mode: ' + EmulatorPage.__mode)
        modelabel.place(relx=0.1, rely=0.1)

        emitterlabel = tk.Label(root, text='Emitter')
        connectionlabel = tk.Label(root, text='Connection')
        receiverlabel = tk.Label(root, text='Receiver')

        emitterlabel.place(relx=0.225, rely=0.1)
        connectionlabel.place(relx=0.475, rely=0.1)
        receiverlabel.place(relx=0.725, rely=0.1)

        emitterlist = tk.Listbox()
        connectionlist = tk.Listbox()
        receiverlist = tk.Listbox()

        EmulatorPage.__listboxes.append(emitterlist)
        EmulatorPage.__listboxes.append(connectionlist)
        EmulatorPage.__listboxes.append(receiverlist)

        emitterlist.place(relx=0.125, rely=0.15, relwidth=0.25, relheight=0.5)
        connectionlist.place(relx=0.375, rely=0.15, relwidth=0.25, relheight=0.5)
        receiverlist.place(relx=0.625, rely=0.15, relwidth=0.25, relheight=0.5)

        emitterseq = tk.Label(root, text='Seq: ')
        receiverseq = tk.Label(root, text='Seq: ')

        EmulatorPage.__seqlabels.append(emitterseq)
        EmulatorPage.__seqlabels.append(receiverseq)

        emitterseq.place(relx=0.125, rely=0.7)
        receiverseq.place(relx=0.625, rely=0.7)

        configbutton = tk.Button(root, text='Configurar')
        configbutton.place(relx=0.125, rely=0.8, relwidth=0.75, relheight=0.05)

        delay = 100
        EmulatorPage.createEmulator()        
        EmulatorPage.setEmitterParams()
        EmulatorPage.setConnectionParams()
        root.after(1, lambda: EmulatorPage.run(delay, root))
        root.mainloop()