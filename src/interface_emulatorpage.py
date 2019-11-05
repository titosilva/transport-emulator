import tkinter as tk

class EmulatorPage:
    @staticmethod
    def setMode(mode: str):
        if mode == 'GBN' or mode == 'SW':
            EmulatorPage.__mode = mode
        else:
            EmulatorPage.__mode = None

    @staticmethod
    def emulate():    
        root = tk.Tk()
        root.title("Welcome to Shiba Emulator :)")

        emitterlabel = tk.Label(root, text='Emitter')
        connectionlabel = tk.Label(root, text='Connection')
        receiverlabel = tk.Label(root, text='Receiver')

        emitterlabel.place(relx=0.225, rely=0.1)
        connectionlabel.place(relx=0.475, rely=0.1)
        receiverlabel.place(relx=0.725, rely=0.1)

        emitterlist = tk.Listbox(root)
        connectionlist = tk.Listbox(root)
        receiverlist = tk.Listbox(root)

        emitterlist.place(relx=0.125, rely=0.15, relwidth=0.25, relheight=0.5)
        connectionlist.place(relx=0.375, rely=0.15, relwidth=0.25, relheight=0.5)
        receiverlist.place(relx=0.625, rely=0.15, relwidth=0.25, relheight=0.5)

        emitterseq = tk.Label(root, text='Seq: ')
        receiverseq = tk.Label(root, text='Expected Seq: ')

        emitterseq.place(relx=0.125, rely=0.7)
        receiverseq.place(relx=0.625, rely=0.7)

        configbutton = tk.Button(root, text='Configurar')
        configbutton.place(relx=0.125, rely=0.8, relwidth=0.75, relheight=0.05)

        root.mainloop()