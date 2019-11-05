import tkinter as tk
import tkinter.messagebox
import interface_emulatorpage as emulpage

HEIGHT = 720
WIDTH = 1280


def button_pressed():
    vazao = vazao_entry.get()
    distancia = distancia_entry.get()
    probabilidade_de_erros = probabilidade_de_erros_entry.get()
    velocidade_da_transmissao = velocidade_da_transmissao_entry.get()
    janela_do_emissor = tamanho_da_janela_do_emissor_entry.get()

    if not(vazao.isdigit()):
        tkinter.messagebox.showinfo('Erro', 'Vazão pode conter apenas números')
    elif not(distancia.isdigit()):
        tkinter.messagebox.showinfo('Erro', 'Distância pode conter apenas números')
    elif not(probabilidade_de_erros.isdigit()):
        tkinter.messagebox.showinfo('Erro', 'Probabilidade de erros pode conter apenas números')
    elif not(velocidade_da_transmissao.isdigit()):
        tkinter.messagebox.showinfo('Erro', 'Velocidade de transmissão pode conter apenas números')
    elif not(janela_do_emissor.isdigit()):
        tkinter.messagebox.showinfo('Erro', 'Tamanho da Janela do Emissor pode conter apenas números')
    else:
        # Inicia a emulação
        emulpage.EmulatorPage.setMode(mode="GBN")
        emulpage.EmulatorPage.emulate()


root = tk.Tk()
root.title("Welcome to Shiba Emulator :)")

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#fce5ac')
frame.place( relwidth = 1, relheight = 1)

#Título
titulo_label = tk.Label(frame, text = "Shiba Emulator", font = 1200, bg='#fce5ac')
titulo_label.place(relx=0.4,rely=0.1,relwidth=0.2, relheight=0.2)

#Vazão
vazao_label = tk.Label(frame, text = "Vazão:", bg='#fce5ac', font = 40)
vazao_label.place(relx=0.157,rely=0.325, relheight=0.05, relwidth=0.1)

vazao_entry = tk.Entry(frame, font = 40)
vazao_entry.place(relx=0.23,rely=0.325,relwidth=0.54, relheight=0.04)

#Distancia
distancia_label = tk.Label(frame, text = "Distância:", bg='#fce5ac', font = 40)
distancia_label.place(relx=0.149,rely=0.395, relheight=0.05, relwidth=0.1)

distancia_entry = tk.Entry(frame, font = 40)
distancia_entry.place(relx=0.23,rely=0.395,relwidth=0.54, relheight=0.04)

#Probabilidade de erros
probabilidade_de_erros_label = tk.Label(frame, text = "Probabilidade de Erros:", bg='#fce5ac', font = 40)
probabilidade_de_erros_label.place(relx=0.085,rely=0.465, relheight=0.05, relwidth=0.15)

probabilidade_de_erros_entry = tk.Entry(frame, font = 40)
probabilidade_de_erros_entry.place(relx=0.23,rely=0.465,relwidth=0.54, relheight=0.04)

#Velocidade da transmissão
velocidade_da_transmissao_label = tk.Label(frame, text = "Velocidade da Transmissão:", bg='#fce5ac', font = 40)
velocidade_da_transmissao_label.place(relx=0.065,rely=0.535, relheight=0.05, relwidth=0.17)

velocidade_da_transmissao_entry = tk.Entry(frame, font = 40)
velocidade_da_transmissao_entry.place(relx=0.23,rely=0.535,relwidth=0.54, relheight=0.04)

#Tamanho da janela do emissor
tamanho_da_janela_do_emissor_label = tk.Label(frame, text = "Tamanho da Janela do Emissor:", bg='#fce5ac', font = 40)
tamanho_da_janela_do_emissor_label.place(relx=0.045,rely=0.605, relheight=0.05, relwidth=0.19)

tamanho_da_janela_do_emissor_entry = tk.Entry(frame, font = 40)
tamanho_da_janela_do_emissor_entry.place(relx=0.23,rely=0.605,relwidth=0.54, relheight=0.04)

# Radio buttons para selecionar modo: GBN ou Stop And Wait

#Botão Emular
button = tk.Button(frame, text="Emular", bg='#FFB778',font=1,activebackground='#E06906', command = button_pressed)
button.place(relx = 0.450, rely = 0.8, relheight=0.05, relwidth=0.1)





root.mainloop()
