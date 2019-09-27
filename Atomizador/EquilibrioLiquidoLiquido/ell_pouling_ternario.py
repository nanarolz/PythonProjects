#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:37:05 2019

@author: mariana
"""
import numpy as np
import scipy.optimize 
import matplotlib.pyplot as plt


# Função de Equilíbrio.
def gamma(x,T):
    z=10
    #v
    Componentes=np.array([ 
                          [0,0,0,0,0,0,1], # álcool
                          [2 , 13.79 , 0 , 1.54 , 0 , 1 , 0], # ester
                          [0,2,1,0,3,0,0]]) # glicerol
    
    Rx = [0.9  , 0.67 , 0.45,1.12,1,1.68,2.11]
    Qx = [0.85 , 0.54 , 0.23 , 0.87,1.2,1.42,1.97]
    
    Interacoes = np.array([[0,0,0,74.54,644.60,972.40,3582.81], #CH3
                           [0,0,0,74.54,644.60,972.40,3582.81], #CH2
                           [0,0,0,74.54,644.60,972.40,3582.81], #CH
                           [292.30,292.30,292.30,0,724.4,-577.50,241.75], #CH--CH
                           [328.2,328.2,328.2,470.7,0,195.6,5299.17], #OH
                           [-320.10,-320.10,-320.10,485.60,180.60,0,-395.51], #CH2COO
                           [-53.92,-53.92,-53.92,-4658.24,-550.58,106.42,0]]) #EtOH
    
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
    
    lnGAMMA2 = np.array(lnGAMMA2) 
    lnGAMMAR = np.sum((Componentes*(lnGAMMA1-lnGAMMA2)),axis=1)
    #---------------------------------------------------------------------FINAL
    
    LnGamma = lnGamaC + lnGAMMAR
    Gamma = np.exp(LnGamma)
    return Gamma


def Equilíbrio(x_global,T,nit = 150):
    #Estimativa do phase split.
    beta = 0.5
    x_phase1 = np.array([0.05,0.05,0.9])
    x_phase2 = (x_global- beta*x_phase1)/(1-beta)
    
    for i in range(nit):
        Gamma_phase1 = gamma(x_phase1,T)
        Gamma_phase2 = gamma(x_phase2,T)
        K=Gamma_phase1/Gamma_phase2
        
        f = lambda beta_new : np.sum(x_global/(beta_new + K*(1-beta_new))) - 1
        beta = scipy.optimize.brentq(f,0,0.95)
        
        x_phase1 = x_global/(beta + K*(1-beta))
        x_phase2 = (x_global- beta*x_phase1)/(1-beta)
        
        if (x_phase1.any() == 0) or (x_phase2.any() == 0):
            break
        
        
    
    return np.array([x_phase1,x_phase2])





