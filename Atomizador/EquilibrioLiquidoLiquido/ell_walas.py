#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:37:05 2019

@author: mariana
"""
import numpy as np

T = 345
x1 = 0.2
x2 = 1 - x1
x = np.array([x1,x2])
z = 10

Componentes = np.array([[1 , 1 , 1 , 0], # Etanol
                        [0 , 0 , 0 , 6]]) # Benzeno

Rx = [0.9011 , 0.6744 , 1.000 , 0.5313]
Qx = [0.8480 , 0.5400 , 1.200 , 0.4000]

Interacoes = np.array([[0.0000 , 0.0000 , 986.5 , 61.130], #CH3
                       [0.0000 , 0.0000 , 986.5 , 61.130], #CH2
                       [156.40 , 156.40 , 0.000 , 89.600], #OH
                       [-11.12 , -11.12 , 636.1 , 0.0000]]) #ArCH

#-----------------------------------------------------------CONFIGURACIONAL
r = np.dot(Componentes,np.transpose(Rx))
q = np.dot(Componentes,np.transpose(Qx))
l = (z*(r-q)/2)-(r-1)
fi = r*x/np.sum(r*x)
ni = q*x/np.sum(q*x)
lnGamaC = np.log(fi/x) + z/2*q*np.log(ni/fi) + l - np.sum(x*l)*fi/x

#------------------------------------------------------------------RESIDUAL
psi = np.exp(-Interacoes/T)

# para a mistura
X = np.dot(np.transpose(Componentes),x)/np.sum(np.dot(np.transpose(Componentes),x))
theta = Qx*X/np.sum(Qx*X)
E = np.dot(theta,psi)
F = np.dot(theta/E,np.transpose(psi))
lnGAMMA1 = Qx*(1 - np.log(E) - F)

# para o componente puro
lnGAMMA2 = []
for i in range(len(x)):
    x_ = np.zeros(len(x))
    x_[i] = 1
    X_ = np.dot(np.transpose(Componentes),x_)/np.sum(np.dot(np.transpose(Componentes),x_))
    theta_ = Qx*X_/np.sum(Qx*X_)
    E_ = np.dot(theta_,psi)
    F_ = np.dot(theta_/E_,np.transpose(psi))
    lnGAMMA_ = Qx*(1 - np.log(E_) - F_)
    lnGAMMA2.append(lnGAMMA_)
    
lnGAMMA2 = np.array(lnGAMMA2) 

lnGAMMAR = np.sum((Componentes*(lnGAMMA1-lnGAMMA2)),axis=1)
#---------------------------------------------------------------------FINAL

LnGamma = lnGamaC + lnGAMMAR
Gamma = np.exp(LnGamma)
for i in range(len(Gamma)):
    print('Gamma', i+1 , ' = ' , Gamma[i])