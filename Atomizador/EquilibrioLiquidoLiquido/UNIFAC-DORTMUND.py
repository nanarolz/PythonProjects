#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:30:22 2019

@author: mariana
"""

import numpy as np
import scipy.optimize 

# Função de Equilíbrio.
def gamma(x,T):
    z=10
    #v
    Componentes=np.array([#CH3 ,   CH2 , CH , CH--CH , OH , CH2COO 
                          [1   , 1     ,  0 ,   0    ,  1 ,      0],  # álcool
                          [2   , 13.79 ,  0 ,   1.54 ,  0 ,      1],  # ester
                          [2   , 1     ,  0 ,   0    ,  3 ,      0]]) # glicerol
    
    #    [  CH3  ,   CH2  ,   CH   , CH--CH ,    OH  , CH2COO]
    Rx = [0.6325 , 0.6325 , 0.6325 , 1.2832 , 1.2302 , 1.2700]
    Qx = [1.0608 , 0.7081 , 0.3554 , 1.2489 , 0.8927 , 1.4228]
    
    # linha i, coluna j
    
    a = np.array([#    CH3 ,     CH2 ,      CH ,  CH--CH ,     OH , CH2COO]
                 [       0 ,       0 ,       0 ,  189.66 , 2777.0 , 98.656],  #CH3
                 [       0 ,       0 ,       0 ,  189.66 , 2777.0 , 98.656],  #CH2
                 [       0 ,       0 ,       0 ,  189.66 , 2777.0 , 98.656],  #CH
                 [ -95.418 , -95.418 , -95.418 ,       0 , 2649.0 , 980.74],  #CH--CH
                 [  1606.0 ,  1606.0 ,  1606.0 ,  1566.0 ,      0 , 973.80],  #OH
                 [  632.22 ,  632.22 ,  632.22 , -582.82 , 310.40 ,      0]]) #CH2COO
    
    b = np.array([#     CH3 ,      CH2 ,       CH ,  CH--CH ,     OH , CH2COO]
                 [        0 ,        0 ,        0 , -0.2723 , -4.674 ,  1.9290],  #CH3
                 [        0 ,        0 ,        0 , -0.2723 , -4.674 ,  1.9290],  #CH2
                 [        0 ,        0 ,        0 , -0.2723 , -4.674 ,  1.9290],  #CH
                 [ -0.06171 , -0.06171 , -0.06171 ,       0 , -6.508 , -2.4224],  #CH--CH
                 [   1606.0 ,   1606.0 ,   1606.0 , -5.8090 ,      0 , -5.6330],  #OH
                 [      4.0 ,      4.0 ,      4.0 ,  1.6732 , 1.5380 ,       0]]) #CH2COO
    
    c = np.array([#     CH3 ,      CH2 ,        CH ,    CH--CH ,        OH ,  CH2COO]
                 [        0 ,        0 ,         0 ,         0 ,   0.00155 ,       0],  #CH3
                 [        0 ,        0 ,         0 ,         0 ,   0.00155 ,       0],  #CH2
                 [        0 ,        0 ,         0 ,         0 ,   0.00155 ,       0],  #CH
                 [        0 ,        0 ,         0 ,         0 ,  0.004822 ,       0],  #CH--CH
                 [ 0.009181 , 0.009181 ,  0.009181 ,  0.005197 ,         0 , 0.00769],  #OH
                 [ 0.003133 , 0.003133 ,  0.003133 ,         0 , -0.004885 ,       0]]) #CH2COO
    
 #-----------------------------------------------------------CONFIGURACIONAL
    r = np.dot(Componentes,np.transpose(Rx))
    q = np.dot(Componentes,np.transpose(Qx))
    l = z*(r-q)/2-(r-1)
    fi = r*(x**(3/4))/np.sum(r*(x**(3/4)))
    ni = q*x/np.sum(q*x)
    lnGamaC = np.log(fi/x) + z/2*q*np.log(ni/fi) + l - np.sum(x*l)*fi/x
    
    #------------------------------------------------------------------RESIDUAL
    psi = np.exp((-a + b*T + c*(T**2))/T)
    
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
    return Gamma


def Equilíbrio(x_global,T,nit = 100):
    #Estimativa do phase split.
    beta = 0.5
    x_phase1 = np.array([0.05 , 0.05 , 0.9])
    
    for i in range(nit):
        x_phase2 = (x_global - (beta*x_phase1))/(1-beta)
        
        Gamma_phase1 = gamma(x_phase1,T)
        Gamma_phase2 = gamma(x_phase2,T)
        K=Gamma_phase1/Gamma_phase2
        
        f = lambda beta_new : np.sum(x_global/(beta_new + K*(1-beta_new))) - 1
        beta = scipy.optimize.newton(f, x0=0.001)
        
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

#x_global=np.array([etanol,ester,glicerol])
x_global = np.array([0.0352,0.4784,0.4864])
T = 313.15
x_eq = Equilíbrio(x_global,T)

np.set_printoptions(precision=4,suppress=True)
print('\n X do equilibrio\n')
print(' 0.0072 0.9740 0.0188')
print(x_eq[1])
print('\n 0.0529 0.0287 0.9184')
print(x_eq[0])