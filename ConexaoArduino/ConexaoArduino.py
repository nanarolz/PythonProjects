# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 21:05:43 2019

@author: maria
"""
import serial
import serial.tools.list_ports

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

conexao.close()