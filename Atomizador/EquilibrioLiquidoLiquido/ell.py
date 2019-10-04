#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:37:05 2019
"""
import numpy as np

x = np.array([0.2066,0.3938,0.3996])
T = 313.15
z=10
#v
Componentes=np.array([#CH3 ,   CH2 , CH , CH--CH , OH , CH2COO 
                      [1   , 1     ,  0 ,   0    ,  1 ,      0], # álcool
                      [2   , 13.79 ,  0 ,   1.54 ,  0 ,      1], # ester
                      [2   , 1     ,  0 ,   0    ,  3 ,      0]]) # glicerol

#    [  CH3  ,   CH2  ,   CH   , CH--CH ,  OH , CH2COO]
Rx = [0.9011 , 0.6744 , 0.4469 , 1.1167 , 1.0 , 1.6764]
Qx = [0.8480 , 0.5400 , 0.2280 , 0.8670 , 1.2 , 1.4200]

Interacoes = np.array([#    CH3 ,     CH2 ,      CH ,   CH--CH ,      OH ,  CH2COO]
                       [      0 ,       0 ,       0 ,    74.54 ,  644.60 ,  972.40], #CH3
                       [      0 ,       0 ,       0 ,    74.54 ,  644.60 ,  972.40], #CH2
                       [      0 ,       0 ,       0 ,    74.54 ,  644.60 ,  972.40], #CH
                       [ 292.30 ,  292.30 ,  292.30 ,        0 ,   724.4 , -577.50], #CH--CH
                       [ 328.20 ,  328.20 ,  328.20 ,   470.70 ,       0 ,  195.60], #OH
                       [-320.10 , -320.10 , -320.10 ,   485.60 ,  180.60 ,       0]]) #CH2COO

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
S=np.dot(x,np.sum(Componentes,axis=1))
X = np.dot(x,Componentes)/S
theta = Qx*X/np.sum(Qx*X)
E = np.dot(theta,psi)
F = np.dot(psi,theta/E)
lnGAMMA1 = Qx*(1 - np.log(E) - F)

# para o componente puro
lnGAMMA2 = []
for i in range(len(x)):
    x_ = np.zeros(len(x))
    x_[i] = 1
    S=np.dot(x_,np.sum(Componentes,axis=1))
    X_ = np.dot(x_,Componentes)/S
    theta_ = Qx*X_/np.sum(Qx*X_)
    E_ = np.dot(theta_,psi)
    F_ = np.dot(psi,theta_/E_)
    lnGAMMA_ = Qx*(1 - np.log(E_) - F_)
    lnGAMMA2.append(lnGAMMA_)

lnGAMMA2 = np.array(lnGAMMA2) 
lnGAMMAR = np.sum((Componentes*(lnGAMMA1-lnGAMMA2)),axis=1)
#---------------------------------------------------------------------FINAL

LnGamma = lnGamaC + lnGAMMAR
Gamma = np.exp(LnGamma)
for i in range(len(Gamma)):
    print('Gamma', i+1 , ' = ' , Gamma[i])