# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 21:05:43 2019

@author: maria
"""
import serial
import serial.tools.list_ports
import time

def serial_ports():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected

conexao = serial.Serial()
conexao.baudrate = 9600
porta = serial_ports()
portastr = str(porta[0])
conexao.port = portastr

conexao.open()
time.sleep(5)
arduinostring = conexao.read(11)
print("Byte: ", arduinostring)
arduinostring = str(arduinostring, 'utf-8')
print("String: ", arduinostring)
dadosarray = arduinostring.split(',')
print(dadosarray[0])
print(dadosarray[1])
tempbanho = float(dadosarray[0])
# a segunda é do banho
tempreator = float(dadosarray[1])
print("Tbanho = ", tempbanho)
print("Treator =", tempreator)
conexao.close()