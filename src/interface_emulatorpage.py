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

    def __End(root: tk.Tk):
        root.destroy()

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
    def setConnectionParams(loss: int, rate: float, distance: float, speed: float)->bool:
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
    def emulate(loss: int=0, rate: float=100000, distance: float=0, speed: float=10000, winsz: int=10):
        root = tk.Tk()
        root.geometry("1280x720")
        root.configure(background='#fce5ac')
        root.title("Welcome to Shiba Emulator :)")

        modelabel = tk.Label(root, text='Mode: ' + EmulatorPage.__mode, bg='#fce5ac')
        modelabel.place(relx=0.1, rely=0.1)

        emitterlabel = tk.Label(root, text='Emitter',bg='#fce5ac', font = 40)
        connectionlabel = tk.Label(root, text='Connection',bg='#fce5ac', font = 40)
        receiverlabel = tk.Label(root, text='Receiver',bg='#fce5ac', font = 40)

        emitterlabel.place(relx=0.225, rely=0.1)
        connectionlabel.place(relx=0.475, rely=0.1)
        receiverlabel.place(relx=0.725, rely=0.1)

        emitterlist = tk.Listbox(root)
        connectionlist = tk.Listbox(root)
        receiverlist = tk.Listbox(root)

        EmulatorPage.__listboxes.append(emitterlist)
        EmulatorPage.__listboxes.append(connectionlist)
        EmulatorPage.__listboxes.append(receiverlist)

        emitterlist.place(relx=0.125, rely=0.15, relwidth=0.25, relheight=0.5)
        connectionlist.place(relx=0.375, rely=0.15, relwidth=0.25, relheight=0.5)
        receiverlist.place(relx=0.625, rely=0.15, relwidth=0.25, relheight=0.5)

        emitterseq = tk.Label(root, text='Seq: ',bg='#fce5ac', font = 40)
        receiverseq = tk.Label(root, text='Expected Seq: ',bg='#fce5ac', font = 40)

        EmulatorPage.__seqlabels.append(emitterseq)
        EmulatorPage.__seqlabels.append(receiverseq)

        emitterseq.place(relx=0.125, rely=0.7)
        receiverseq.place(relx=0.625, rely=0.7)

        configbutton = tk.Button(root, text='Exit',activebackground='#E06906', bg='#FFB778',font=1, command= lambda: EmulatorPage.__End(root))
        configbutton.place(relx=0.125, rely=0.8, relwidth=0.75, relheight=0.05)

        delay = 100
        EmulatorPage.createEmulator()   
        # Usando 41 como tamanho medio dos pacotes, pois todos os pacotes
        # usam b'This is a test packet' como dados e header padrao de 20 bytes
        timeout=2.1*(41/rate + distance/speed)
        EmulatorPage.setEmitterParams(winsz, timeout)
        EmulatorPage.setConnectionParams(loss, rate, distance, speed)
        root.after(0, lambda: EmulatorPage.run(delay, root))
        root.mainloop()