#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:37:05 2019
"""
import numpy as np
import scipy.optimize 

# Função de Equilíbrio.
def gamma(x,T):
    z=10
    #v
    Componentes=np.array([#CH3 , CH2 , CH , CH--CH , OH , CH2COO 
                          [1 , 1     , 0 , 0    , 1 , 0 ], # álcool
                          [2 , 13.79 , 0 , 1.54 , 0 , 1 ], # ester
                          [0 , 2     , 1 , 0    , 3 , 0 ]]) # glicerol
    
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
    X = np.dot(np.transpose(Componentes),x)/np.sum(np.dot(np.transpose(Componentes),x))
    theta = Qx*X/np.sum(Qx*X)
    E = np.dot(psi,theta)
    F = np.dot(theta/E,psi)
    lnGAMMA1 = Qx*(1 - np.log(E) - F)
    
    # para o componente puro
    lnGAMMA2 = []
    for i in range(len(x)):
        x_ = np.zeros(len(x))
        x_[i] = 1
        X_ = np.dot(np.transpose(Componentes),x_)/np.sum(np.dot(np.transpose(Componentes),x_))
        theta_ = Qx*X_/np.sum(Qx*X_)
        E_ = np.dot(psi,theta_)
        F_ = np.dot(theta_/E_,psi)
        lnGAMMA_ = Qx*(1 - np.log(E_) - F_)
        lnGAMMA2.append(lnGAMMA_)
    
    lnGAMMA2 = np.array(lnGAMMA2) 
    lnGAMMAR = np.sum((Componentes*(lnGAMMA1-lnGAMMA2)),axis=1)
    #---------------------------------------------------------------------FINAL
    
    LnGamma = lnGamaC + lnGAMMAR
    Gamma = np.exp(LnGamma)
    return Gamma


def Equilíbrio(x_global,T,nit = 100):
    #Estimativa do phase split.
    beta = 0.5
    x_phase1 = np.array([0.05 , 0.05 , 0.90])
    
    for i in range(nit):
        x_phase2 = (x_global - (beta*x_phase1))/(1-beta)
        
        Gamma_phase1 = gamma(x_phase1,T)
        Gamma_phase2 = gamma(x_phase2,T)
        K=Gamma_phase1/Gamma_phase2
        
        f = lambda beta_new : np.sum(x_global/(beta_new + K*(1-beta_new))) - 1
        beta = scipy.optimize.newton(f, x0=0.01)
        
        x_phase1 = x_global/(beta + (K*(1-beta)))
        
    return np.array([x_phase1,x_phase2])

#x_global=np.array([etanol,ester,glicerol])
x_global = np.array([0.2066,0.3938,0.3996])
T = 313.15
x_eq = Equilíbrio(x_global,T)

np.set_printoptions(precision=4,suppress=True)
print('\n X do equilibrio\n')
print(' 0.1061 0.8690 0.0249')
print(x_eq[1])
print('\n 0.2856 0.0211 0.6933')
print(x_eq[0])