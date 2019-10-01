#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:37:05 2019

@author: mariana
"""
import numpy as np

T = 307
x1 = 0.047
x2 = 1 - x1
x = np.array([x1,x2])
z = 10

#v
Componentes = np.array([[1 , 1 , 0], # acetona
                        [2 , 0 , 3]]) # n-pentano

Rx = [0.9011 , 1.6724 , 0.6744]
Qx = [0.8480 , 1.4880 , 0.5400]

#a
Interacoes = np.array([[0.0000 , 476.40 , 0.000], #CH3
                       [26.760 , 0.0000 , 26.760], #CH3CO
                       [0.0000 , 476.40 , 0.000]]) #CH2

#-----------------------------------------------------------CONFIGURACIONAL
r = np.dot(Componentes,np.transpose(Rx))
q = np.dot(Componentes,np.transpose(Qx))
l = z*(r-q)/2-(r-1)
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

# formatando lngamma
aux = Componentes[:]
for i in range(np.size(aux,0)):
    for j in range(np.size(aux,1)):
        if (aux[i,j] != 0):
            aux[i,j] = 1

lnGAMMA2 =aux*lnGAMMA2
lnGAMMA1 = aux*lnGAMMA1

lnGAMMA2 = np.array(lnGAMMA2) 
lnGAMMAR = np.sum((Componentes*(lnGAMMA1-lnGAMMA2)),axis=1)
#---------------------------------------------------------------------FINAL

LnGamma = lnGamaC + lnGAMMAR
Gamma = np.exp(LnGamma)
for i in range(len(Gamma)):
    print('Gamma', i+1 , ' = ' , Gamma[i])