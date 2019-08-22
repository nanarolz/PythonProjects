#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:51:15 2019

@author: mariana góis
"""

#---------------------------------------------------------------BIBLIOTECAS

import serial
import time
import threading

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
import serial.tools.list_ports

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#-----------------------------------------------------------------VARIÁVEIS

desligado = '#c0392b'
ligado = '#2ecc71'
cordefundo = '#ecf0f1'
portastr = ' '

lista_tempo = []
lista_treator = []
lista_tbanho = []

#-------------------------------------------------------------------GRÁFICO
fig = Figure()
grafico = fig.add_subplot(111)
 
#---------------------------------------------------------FUNÇÃO DOS BOTÕES
def serial_ports():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected

def arduinoonoff():
    if btarduino["text"] == "PLACA ON":
        btarduino["text"] = "PLACA OFF"
        btarduino["bg"] = desligado
        conexao.close()
    else:
        porta = serial_ports()

        if not serial_ports():
            messagebox.showinfo("Erro", "Arduino não reconhecido. Conecte-o ou utilize outra porta de comunicação")
        else:
            btarduino["text"] = "PLACA ON"
            btarduino["bg"] = ligado
            portastr = str(porta[0])
            conexao.port = portastr
            lbporta["text"] = " PORTA: " + portastr
            conexao.open()

        
def mudarporta():
    lbporta["text"] = " PORTA: " + edporta.get()
    portastr = edporta.get()
    conexao.port = portastr
    
def mudarsetpoint():
    lbtempsp["text"] = edsetpoint.get()
    # setpoint = edsetpoint.get()
        
def ligabombareator():
    if btreator["bg"] == desligado:
        conexao.write(b'a') # liga
        btreator["bg"] = ligado
    else:
        conexao.write(b'b') # desliga
        btreator["bg"] = desligado

def ligabombaresfriador():
    if bttrocador["bg"] == desligado:
        conexao.write(b'c') # liga
        bttrocador["bg"] = ligado
    else:
        conexao.write(b'd') # desliga
        bttrocador["bg"] = desligado
    
def ligasolenoide():
    if btatomizador["bg"] == desligado:
        conexao.write(b'l') # liga
        btatomizador["bg"] = ligado
    else:
        conexao.write(b'm') # desliga
        btatomizador["bg"] = desligado

def adquirirdados():
    contador_tempo = 0
    while True:
        arduinostring = conexao.readline()
        arduinostring = str(arduinostring, 'utf-8')
        dadosarray = arduinostring.split(',')
        tempreator = float(dadosarray[0])
        tempbanho = float(dadosarray[1])
        lista_treator.append(tempreator)
        lista_tbanho.append(tempbanho)
        lbtemp1["text"] = tempreator
        lbtemp2["text"] = tempbanho    
        
        lista_tempo.extend([contador_tempo])
        
        contador_tempo = contador_tempo + 1
        
        grafico.cla()
        configuracoesgrafico()
        canvas.draw_idle()

        time.sleep(1)
        
        if parar:
            break;
    #print("parada aquisição")
          
def aquisicaodados():
    if btdados["bg"] == desligado:
        btdados["bg"] = ligado
        t1 = threading.Thread(target=adquirirdados)
        t1.daemon = True
        global parar
        parar = False
        t1.start()
    else:
        btdados["bg"] = desligado
        parar = True
    
def sair():
    conexao.close()
    janela.quit()     
    janela.destroy()

def salvar():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None:
        return
    f.write("Tempo(s) , T reator , T banho\n")
    output = '\n'.join('\t'.join(map(str,row)) for row in zip(
            lista_tempo, lista_treator, lista_tbanho))
    f.write(output)
    f.close()

def configuracoesgrafico():
    grafico.set_title("Monitoramento da Temperatura")
    grafico.set_xlabel("Tempo (s)")
    grafico.set_ylabel("Temperatura (ºC)")
    grafico.set_ylim(0,160)
    grafico.grid()
    grafico.plot(lista_tempo, lista_treator, 'ro-', 
                 label='Temperatura do reator')
    grafico.plot(lista_tempo, lista_tbanho, 'b^-', 
                 label='Temperatura do banho')
    grafico.legend(loc='upper left')

def resetardados():
    lista_tempo.clear()
    lista_treator.clear()
    lista_tbanho.clear()
    grafico.cla()
    configuracoesgrafico()
    canvas.draw_idle()
    
#---------------------------------------------------CONFIGURAÇÕES DA JANELA

janela = Tk() # criando
janela.title("Reator de atomização") # nomeando
janela["bg"] = cordefundo # cor de fundo 
#janela.state("zoomed") # fullscreen
#janela.overrideredirect(1) # remove a barra de cima
#janela.resizable(0,0) # remove maximização

janela.geometry("925x600+200+200") # LarguraxAltura+E+T

#-------------------------------------------------------------PORTA ARDUINO

conexao = serial.Serial()
conexao.baudrate = 9600
#porta = serial_ports()
#portastr = str(porta[0])
#conexao.port = portastr

#--------------------------------------------------------------------BOTÕES

btdados = Button(janela, width=18, height=2, text="AQUISIÇÃO DE DADOS", 
                 bg=desligado, command=aquisicaodados, fg="white")
btdados.grid(row=0,column=3, sticky="nsew")

btreator = Button(janela, width=18, height=2, text="BOMBA DO REATOR", 
                  bg=desligado, command=ligabombareator, fg="white")
btreator.grid(row=0,column=4, sticky="nsew")

bttrocador = Button(janela, width=18, height=2, text="BOMBA DO TROCADOR", 
                    bg=desligado, command=ligabombaresfriador, fg="white")
bttrocador.grid(row=0,column=5, sticky="nsew")

btatomizador = Button(janela, width=18, height=2, text="ATOMIZADOR", 
                      bg=desligado, command=ligasolenoide, fg="white")
btatomizador.grid(row=0,column=6, sticky="nsew")

btcompressor = Button(janela, width=18, height=2, text="RESETAR DADOS", 
                      bg="#34495e", fg="white", command=resetardados)
btcompressor.grid(row=0,column=7, sticky="nsew")

btarduino = Button(janela, width=18, height=2, text="PLACA OFF", 
                   bg=desligado, command=arduinoonoff, fg="white")
btarduino.grid(row=0,column=0, sticky="nsew", columnspan=3)

lbporta = Label(janela, text="PORTA: " + portastr, bg=cordefundo)
lbporta.grid(row=1,column=0, sticky="nsew", columnspan=3)

edporta = Entry(janela)
edporta.grid(row=2,column=0, sticky="nsew", columnspan=3)

btporta = Button(janela, width=18, height=2, text="MUDAR PORTA", 
                 command=mudarporta)
btporta.grid(row=3,column=0, sticky="nsew", columnspan=3)

configuracoesgrafico()
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().grid(row=1,column=3, columnspan=5, rowspan=22, 
                    sticky="nsew") 
#------------------------------------------------------------------CONTROLE

lbcontrole = Label(janela, text="CONTROLE", bg=cordefundo, 
                   font=("Helvetica", 20))
lbcontrole.grid(row=4,column=0, sticky="nsew", columnspan=3)

btporta = Button(janela, width=18, height=2, text="AUTOMÁTICO", 
                 bg=desligado, fg="white")
btporta.grid(row=5,column=0, sticky="nsew", columnspan=3)

#---------------------------------------------------------------TEMPERATURA

lbsetpoint = Label(janela, text="SetPoint: ", bg=cordefundo,
                   font=("Helvetica", 16))
lbsetpoint.grid(row=6,column=0, columnspan=2)

lbtempsp = Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtempsp.grid(row=6,column=2)

edsetpoint = Entry(janela)
edsetpoint.grid(row=7,column=0, sticky="nsew", columnspan=3)

btsetpoint = Button(janela, width=18, height=2, text="SET-POINT", 
                 command=mudarsetpoint, bg=desligado, fg="white")
btsetpoint.grid(row=8,column=0, sticky="nsew", columnspan=3)

lbrotulotemp1 = Label(janela, text="Treator:", bg=cordefundo,
                      font=("Helvetica", 16))
lbrotulotemp1.grid(row=9,column=0, columnspan=2)

lbtemp1 = Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtemp1.grid(row=9,column=2)

lbrotulotemp2 = Label(janela, text="Tbanho:", bg=cordefundo,
                      font=("Helvetica", 16))
lbrotulotemp2.grid(row=10, column=0, columnspan=2)

lbtemp2 = Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtemp2.grid(row=10,column=2)

#---------------------------------------------------------------------DADOS
'''
lbtempo = Label(janela, text="Tempo", bg=cordefundo, font=("Helvetica", 12))
lbtempo.grid(row=11,column=0)

lbtempo = Label(janela, text="Tbanho", bg=cordefundo, font=("Helvetica", 12))
lbtempo.grid(row=11,column=1)

lbtempo = Label(janela, text="Treator", bg=cordefundo, font=("Helvetica", 12))
lbtempo.grid(row=11,column=2)

for x in range(12,22):
    for y in range(0,3):
        lbtempo = Label(janela, text="-", bg=cordefundo, 
                        font=("Helvetica", 12))
        lbtempo.grid(row=x,column=y, sticky="nsew")
'''
#---------------------------------------------------------JANELA RESPONSIVA

for x in range(3,8):
    Grid.columnconfigure(janela, x, weight=1)
for y in range(23):
    Grid.rowconfigure(janela, y, weight=1)

#---------------------------------------------------------------------FINAL
   
btsalvar= Button(janela, text="SALVAR DADOS EM CSV", command=salvar, 
                 height=2, bg="#34495e", fg="white")
btsalvar.grid(row=23,column=0, sticky="nsew", columnspan=3)

btfinal= Button(janela, text="SAIR", command=sair)
btfinal.grid(row=23,column=3, columnspan=5, sticky="nsew")

janela.mainloop() # enquanto a janela estiver aberta não executa nada depois
