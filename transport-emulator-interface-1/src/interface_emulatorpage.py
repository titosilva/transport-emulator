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
        root.geometry("1280x720")
        root.configure(background='#fce5ac')
        root.title("Welcome to Shiba Emulator :)")

        emitterlabel = tk.Label(root, text='Emitter',bg='#fce5ac', font = 40)
        connectionlabel = tk.Label(root, text='Connection',bg='#fce5ac', font = 40)
        receiverlabel = tk.Label(root, text='Receiver',bg='#fce5ac', font = 40)

        emitterlabel.place(relx=0.225, rely=0.1)
        connectionlabel.place(relx=0.475, rely=0.1)
        receiverlabel.place(relx=0.725, rely=0.1)

        emitterlist = tk.Listbox(root)
        connectionlist = tk.Listbox(root)
        receiverlist = tk.Listbox(root)

        emitterlist.place(relx=0.125, rely=0.15, relwidth=0.25, relheight=0.5)
        connectionlist.place(relx=0.375, rely=0.15, relwidth=0.25, relheight=0.5)
        receiverlist.place(relx=0.625, rely=0.15, relwidth=0.25, relheight=0.5)

        emitterseq = tk.Label(root, text='Seq: ',bg='#fce5ac', font = 40)
        receiverseq = tk.Label(root, text='Expected Seq: ',bg='#fce5ac', font = 40)

        emitterseq.place(relx=0.125, rely=0.7)
        receiverseq.place(relx=0.625, rely=0.7)

        configbutton = tk.Button(root, text='Configurar',activebackground='#E06906', bg='#FFB778',font=1)
        configbutton.place(relx=0.125, rely=0.8, relwidth=0.75, relheight=0.05)

        root.mainloop()