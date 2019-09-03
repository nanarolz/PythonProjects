#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:51:15 2019

@author: mariana góis
"""

#---------------------------------------------------------------BIBLIOTECAS
# comunicacao arduino
import serial
import serial.tools.list_ports
# temporizador
import time
# rodar funções em segundo plano
import threading
# janela
import tkinter
from tkinter import filedialog
from tkinter import messagebox
# exiibir grafico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#-----------------------------------------------------------------VARIÁVEIS
# atributos
desligado = '#c0392b'
ligado = '#2ecc71'
cordefundo = '#ecf0f1'
portastr = ' '
# arduino
conexao = serial.Serial()
conexao.baudrate = 9600
conexao.timeout = 5
# listas
lista_tempo = []
lista_treator = []
lista_tbanho = []
# controle
SP = None
tempreator = None
pararcontroleautomatico = None
Kcp = 3.03
Kc1 = 36.629
tau_i = 4024
# grafico
fig = Figure()
grafico = fig.add_subplot(111)
# aquisição de dados
parar = None
# salvar em arquivo
f = open("dados.csv", "a+")
f.write("Tempo(s) , T reator , T banho\n")
f.close()
#---------------------------------------------------------FUNÇÃO DOS BOTÕES
def serial_ports(): # detectar automaticamente a porta serial
    # pega as portas do sistema
    comlist = serial.tools.list_ports.comports()
    # lista das conectadas
    conectados = []
    for element in comlist:
        # coloca na lista aquelas que estao conectadas
        conectados.append(element.device)
    return conectados

def arduinoonoff():
    if btarduino["text"] == "PLACA ON":
        btarduino["text"] = "PLACA OFF"
        btarduino["bg"] = desligado
        # fecha a conexao
        conexao.close()
    else:
        # chama a funcao para verificar automaticamente as portas
        porta = serial_ports()
        # verifica se há conexao
        if not serial_ports():
            messagebox.showinfo("Erro", "Arduino não reconhecido. Conecte-o ou utilize outra porta de comunicação")
        else:
            # conecta ao arduino
            btarduino["text"] = "PLACA ON"
            btarduino["bg"] = ligado
            # pega a primeira conexao disponivel no array
            portastr = str(porta[0])
            # define a porta a ser conectada
            conexao.port = portastr
            # imprime na janela
            lbporta["text"] = " PORTA: " + portastr
            # abre a conexao 
            conexao.open()
            time.sleep(1)

def mudarporta():
    lbporta["text"] = " PORTA: " + edporta.get()
    # pega a porta digitada
    portastr = edporta.get()
    # seta a porta
    conexao.port = portastr
    
def mudarsetpoint():
    global SP
    # pega o set point definido
    SP = edsetpoint.get()
    # imprime o set point na janela
    lbtempsp["text"] = SP
    SP = int(SP)
    # verifica se o set point foi colocado
    if not SP:
        messagebox.showinfo("Erro", "Defina a temperatura (ºC) do set point.")
        
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
       
        while True: 
           try:
               conexao.flushInput()
               time.sleep(1)
               conexao.write(b'g') # liga
               # le uma linha do arduino
               arduinostring = conexao.readline()
               # transforma os bites em string
               arduinostring = str(arduinostring, 'utf-8')
               # separa as duas temperaturas
               dadosarray = arduinostring.split(',')
               # a primeira é do banho
               global tempbanho
               tempbanho = float(dadosarray[0])
               # a segunda é do reator
               global tempreator
               tempreator = float(dadosarray[1])
               break
           except ValueError:
               print("Erro de aquisição - Utilizar dados anteriores.")
               if len(lista_treator)!=0:
                   lista_treator.append(lista_treator[-1])
                   lista_tbanho.append(lista_tbanho[-1])
                   lista_tempo.append(lista_tempo[-1]+1)
                   
        # adiciona na lista das temperaturas do reator
        lista_treator.append(tempreator)
        
        #lista_treator.append(lista_treator[-1])
        
        # adiciona na lista de temperatura do banho
        lista_tbanho.append(tempbanho)
        # imprime as temperaturas na janela
        lbtemp1["text"] = tempreator
        lbtemp2["text"] = tempbanho  
        lbtempodecorrido["text"] = contador_tempo
        # adiciona na lista do tempo o contador temporal
        lista_tempo.extend([contador_tempo])
        # incrementa o tempo
        contador_tempo = contador_tempo + 5
        # reseta o grafico
        grafico.cla()
        # chama a funcao para refazer novamente
        configuracoesgrafico()
        # desenha o grafico na janela
        canvas.draw_idle()
        # flag de parada da função em segundo plano
        time.sleep(4)
        if parar:
            break;
    #print("parada aquisição")
          
def aquisicaodados():
    if btdados["bg"] == desligado:
        btdados["bg"] = ligado
        # aciona a aquisicao de dados no background
        t1 = threading.Thread(target=adquirirdados)
        t1.daemon = True
        # flag de parada como falsa
        global parar
        parar = False
        t1.start()
    else:
        btdados["bg"] = desligado
        #flag de parada como verdadeira
        parar = True
    
def sair():
    # fecha a conexão com o arduino
    conexao.close()
    # fecha a janela
    janela.quit()   
    # destroi qualquer funcao que ainda esteja em execução
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
    grafico.set_ylim(0,100)
    grafico.grid()
    grafico.minorticks_on()
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

def controle():
    if not SP:
        messagebox.showinfo("Erro", "Defina a temperatura (ºC) do set point.")
    elif not conexao.isOpen():
        messagebox.showinfo("Erro", "Arduino não reconhecido. Conecte-o ou utilize outra porta de comunicação")
    elif btcontrole["bg"] == ligado:
        btcontrole["bg"] = desligado
        conexao.write(b'R000')
        time.sleep(1)
        conexao.write(b'j000')
        global pararcontroleautomatico
        pararcontroleautomatico = True
        print("desligado")
    else:
        btcontrole["bg"] = ligado
        print("rodando")
        pararcontroleautomatico = False
        # aciona o controle automatico no background
        t2 = threading.Thread(target=controleautomatico)
        t2.daemon = True
        t2.start()
        
def controleautomatico():
    soma = 0
    contador_condensador = 0
    erro_anterior = 0
    dt = 5
    tempo_condensador = 120/dt;
    while True:
        # flag de parada da função em segundo plano
        erro = SP - tempreator # calcula o erro
        soma = soma + (erro + erro_anterior)*dt/2
        contador_condensador = contador_condensador + 1

        if erro > 0:
            # resistencias
            lbstatus["text"] = "resistência on"
            
            R = Kcp * erro

            if R < 0: # resistencia menor que 0%
                R = 0
    
            if R > 100: # resistencia maior que 100%
                R = 100
                
            R = int(R)
            
            if R < 10:
                R = str(R) # convertendo para string
                R = '00' + R
            
            elif (R >= 10) and (R <= 99):
                R = str(R) # convertendo para string
                R = '0' + R
            else:
                R = str(R) # convertendo para string
            
            lbpercentual["text"] = R
            R = 'R' + R # adicionando caractere
            #R.encode('utf-8')
            conexao.write(bytes(R,'utf-8'))
            
            contador_condensador = 0
            
        else:
            # condensador 
            lbstatus["text"] = "condensador on"
                
            conexao.write(b'R000')
    
            C = -Kc1 * ( erro + (1 / tau_i) * soma )
    
            if C < 0: 
                C = 0
                
            if C > 100:
                C = 100
    
            if(contador_condensador > tempo_condensador): # passado 120 segundos
            
                contador_condensador = 0
        
                C = str(C) # convertendo para string
                lbpercentual["text"] = C[0:4]
                C = 'j' + C # adicionando caractere
                conexao.write(bytes(C, 'UTF-8'))
    
        erro_anterior = erro
        time.sleep(dt)

        if pararcontroleautomatico:
            conexao.write(b'R000')
            conexao.write(b'j000')
            print("controle desligado")
            break;
    #print("parada aquisição")
        
#---------------------------------------------------CONFIGURAÇÕES DA JANELA

janela = tkinter.Tk() # criando
janela.title("Reator de atomização") # nomeando
janela["bg"] = cordefundo # cor de fundo 
#janela.state("zoomed") # fullscreen
#janela.overrideredirect(1) # remove a barra de cima
#janela.resizable(0,0) # remove maximização

janela.geometry("925x600+200+200") # LarguraxAltura+E+T

#--------------------------------------------------------------------BOTÕES

btdados = tkinter.Button(janela, width=18, height=2, text="AQUISIÇÃO DE DADOS", 
                 bg=desligado, command=aquisicaodados, fg="white")
btdados.grid(row=0,column=3, sticky="nsew")

btreator = tkinter.Button(janela, width=18, height=2, text="BOMBA DO REATOR", 
                  bg=desligado, command=ligabombareator, fg="white")
btreator.grid(row=0,column=4, sticky="nsew")

bttrocador = tkinter.Button(janela, width=18, height=2, text="BOMBA DO TROCADOR", 
                    bg=desligado, command=ligabombaresfriador, fg="white")
bttrocador.grid(row=0,column=5, sticky="nsew")

btatomizador = tkinter.Button(janela, width=18, height=2, text="ATOMIZADOR", 
                      bg=desligado, command=ligasolenoide, fg="white")
btatomizador.grid(row=0,column=6, sticky="nsew")

btcompressor = tkinter.Button(janela, width=18, height=2, text="RESETAR DADOS", 
                      bg="#34495e", fg="white", command=resetardados)
btcompressor.grid(row=0,column=7, sticky="nsew")

btarduino = tkinter.Button(janela, width=18, height=2, text="PLACA OFF", 
                   bg=desligado, command=arduinoonoff, fg="white")
btarduino.grid(row=0,column=0, sticky="nsew", columnspan=3)

lbporta = tkinter.Label(janela, text="PORTA: " + portastr, bg=cordefundo)
lbporta.grid(row=1,column=0, sticky="nsew", columnspan=3)

edporta = tkinter.Entry(janela)
edporta.grid(row=2,column=0, sticky="nsew", columnspan=3)

btporta = tkinter.Button(janela, width=18, height=2, text="MUDAR PORTA", 
                 command=mudarporta)
btporta.grid(row=3,column=0, sticky="nsew", columnspan=3)

#-------------------------------------------------------------------GRAFICO

configuracoesgrafico()
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().grid(row=1,column=3, columnspan=5, rowspan=22, 
                    sticky="nsew") 

#------------------------------------------------------------------CONTROLE

lbcontrole = tkinter.Label(janela, text="CONTROLE", bg=cordefundo, 
                   font=("Helvetica", 20))
lbcontrole.grid(row=4,column=0, sticky="nsew", columnspan=3)

btcontrole = tkinter.Button(janela, width=18, height=2, text="AUTOMÁTICO", 
                 bg=desligado, fg="white", command=controle)
btcontrole.grid(row=5,column=0, sticky="nsew", columnspan=3)

#---------------------------------------------------------------TEMPERATURA

lbsetpoint = tkinter.Label(janela, text="SetPoint: ", bg=cordefundo,
                   font=("Helvetica", 16))
lbsetpoint.grid(row=6,column=0, columnspan=2)

lbtempsp = tkinter.Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtempsp.grid(row=6,column=2)

edsetpoint = tkinter.Entry(janela)
edsetpoint.grid(row=7,column=0, sticky="nsew", columnspan=3)

btsetpoint = tkinter.Button(janela, width=18, height=2, text="SET-POINT", 
                 command=mudarsetpoint, bg=desligado, fg="white")
btsetpoint.grid(row=8,column=0, sticky="nsew", columnspan=3)

lbrotulotemp1 = tkinter.Label(janela, text="Treator:", bg=cordefundo,
                      font=("Helvetica", 16))
lbrotulotemp1.grid(row=9,column=0, columnspan=2)

lbtemp1 = tkinter.Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtemp1.grid(row=9,column=2)

lbrotulotemp2 = tkinter.Label(janela, text="Tbanho:", bg=cordefundo,
                      font=("Helvetica", 16))
lbrotulotemp2.grid(row=10, column=0, columnspan=2)

lbtemp2 = tkinter.Label(janela, text="-", bg=cordefundo, font=("Helvetica", 16))
lbtemp2.grid(row=10,column=2)

#---------------------------------------------------------------------DADOS

lbstatus = tkinter.Label(janela, text="STATUS", bg=cordefundo, font=("Helvetica", 12))
lbstatus.grid(row=11,column=0,columnspan=3)

lbpercentual = tkinter.Label(janela, text="00.00", bg=cordefundo, font=("Helvetica", 12))
lbpercentual.grid(row=12,column=0,columnspan=2)

lbporcentagem = tkinter.Label(janela, text="%", bg=cordefundo, font=("Helvetica", 12))
lbporcentagem.grid(row=12,column=2)

lbtempo = tkinter.Label(janela, text="TEMPO OPERAÇÃO (s)", bg=cordefundo,
                        font=("Helvetica", 12))
lbtempo.grid(row=13,column=0,columnspan=3)

lbtempodecorrido = tkinter.Label(janela, text="0", bg=cordefundo,
                        font=("Helvetica", 12))
lbtempodecorrido.grid(row=14,column=0,columnspan=3)

'''
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
    tkinter.Grid.columnconfigure(janela, x, weight=1)
for y in range(23):
    tkinter.Grid.rowconfigure(janela, y, weight=1)

#---------------------------------------------------------------------FINAL
   
btsalvar= tkinter.Button(janela, text="SALVAR DADOS EM CSV", command=salvar, 
                 height=2, bg="#34495e", fg="white")
btsalvar.grid(row=23,column=0, sticky="nsew", columnspan=3)

btfinal= tkinter.Button(janela, text="SAIR", command=sair)
btfinal.grid(row=23,column=3, columnspan=5, sticky="nsew")

janela.mainloop() # enquanto a janela estiver aberta não executa nada depois
