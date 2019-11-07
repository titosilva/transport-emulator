import tkinter as tk
import tkinter.messagebox
import interface_emulatorpage as emulpage

HEIGHT = 720
WIDTH = 1280

def is_num(s):
    ##Returns True is string is a number.
    try:
        float(s)
        return True
    except ValueError:
        return False

def button_pressed():
    vazao = vazao_entry.get()
    distancia = distancia_entry.get()
    probabilidade_de_erros = probabilidade_de_erros_entry.get()
    velocidade_da_transmissao = velocidade_da_transmissao_entry.get()
    janela_do_emissor = tamanho_da_janela_do_emissor_entry.get()

    if not(is_num(vazao)):
        tkinter.messagebox.showinfo('Erro', 'Vazão pode conter apenas números')
    elif not(is_num(distancia)):
        tkinter.messagebox.showinfo('Erro', 'Distância pode conter apenas números')
    elif not(is_num(probabilidade_de_erros)):
        tkinter.messagebox.showinfo('Erro', 'Probabilidade de erros pode conter apenas números')
    elif not(is_num(velocidade_da_transmissao)):
        tkinter.messagebox.showinfo('Erro', 'Velocidade de transmissão pode conter apenas números')
    elif not(is_num(janela_do_emissor)):
        tkinter.messagebox.showinfo('Erro', 'Tamanho da Janela do Emissor pode conter apenas números')
    else:
        # Pega os parametros
        vazao = float(vazao)
        distancia = float(distancia)
        probabilidade_de_erros = float(probabilidade_de_erros)
        velocidade_da_transmissao = float(velocidade_da_transmissao)
        janela_do_emissor = int(janela_do_emissor)

        # Pega o protocolo selecionado
        value = var.get()
        if value==1:
            emulpage.EmulatorPage.setMode(mode="SW")
        elif value==2:
            emulpage.EmulatorPage.setMode(mode="GBN")
        else:
            tkinter.messagebox.showinfo('Erro', 'Selecione um tipo de protocolo')
            return

        # Inicia a emulação
        root.destroy()
        emulpage.EmulatorPage.emulate(probabilidade_de_erros, vazao, distancia, velocidade_da_transmissao, janela_do_emissor)
        return
        

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
vazao_label = tk.Label(frame, text = "Throughput: ", bg='#fce5ac', font = 40)
vazao_label.place(relx=0.18 ,rely=0.325, relheight=0.05, relwidth=0.1)

vazao_entry = tk.Entry(frame, font = 40)
vazao_entry.place(relx=0.28,rely=0.325,relwidth=0.54, relheight=0.04)

#Distancia
distancia_label = tk.Label(frame, text = "Distance: ", bg='#fce5ac', font = 40)
distancia_label.place(relx=0.187,rely=0.395, relheight=0.05, relwidth=0.1)

distancia_entry = tk.Entry(frame, font = 40)
distancia_entry.place(relx=0.28,rely=0.395,relwidth=0.54, relheight=0.04)

#Probabilidade de erros
probabilidade_de_erros_label = tk.Label(frame, text = "Error Probability:  ", bg='#fce5ac', font = 40)
probabilidade_de_erros_label.place(relx=0.111,rely=0.465, relheight=0.05, relwidth=0.2)

probabilidade_de_erros_entry = tk.Entry(frame, font = 40)
probabilidade_de_erros_entry.place(relx=0.28,rely=0.465,relwidth=0.54, relheight=0.04)

#Velocidade da transmissão
velocidade_da_transmissao_label = tk.Label(frame, text = "Transmission Speed:", bg='#fce5ac', font = 40)
velocidade_da_transmissao_label.place(relx=0.083,rely=0.535, relheight=0.05, relwidth=0.22)

velocidade_da_transmissao_entry = tk.Entry(frame, font = 40)
velocidade_da_transmissao_entry.place(relx=0.28,rely=0.535,relwidth=0.54, relheight=0.04)

#Tamanho da janela do emissor
tamanho_da_janela_do_emissor_label = tk.Label(frame, text = "Emitter Window Size:", bg='#fce5ac', font = 40)
tamanho_da_janela_do_emissor_label.place(relx=0.06,rely=0.605, relheight=0.05, relwidth=0.27)

tamanho_da_janela_do_emissor_entry = tk.Entry(frame, font = 40)
tamanho_da_janela_do_emissor_entry.place(relx=0.279,rely=0.605,relwidth=0.54, relheight=0.04)

# Radio buttons para selecionar modo: GBN ou Stop And Wait
var = tk.IntVar()

radiosw = tk.Radiobutton(root, text='Stop-and-Wait', variable=var, value=1, bg='#fce5ac')
radiogbn = tk.Radiobutton(root, text='Go-Back-N', variable=var, value=2, bg='#fce5ac')

radiosw.place(relx=0.28, rely=0.7)
radiogbn.place(relx=0.28, rely=0.75)

#Botão Emular
button = tk.Button(frame, text="Emulate", bg='#FFB778',font=1,activebackground='#E06906', command = button_pressed)
button.place(relx = 0.450, rely = 0.8, relheight=0.05, relwidth=0.1)


root.mainloop()