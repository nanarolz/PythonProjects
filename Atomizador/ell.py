#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:23:56 2019

@author: mariana
"""

import numpy as np

#Utilizando a seguinte notação:
#1 - óleo de Girassol 
#2 - Álcool
#3 - Ester 
#4 - Glicerol
 
def gamma(T,x1,x2,x3,x4):
    #Colunas
    #1 - CH3
    #2 - CH2
    #3 - CH
    #4 - CH--CH
    #5 - OH
    #6 - CH2COO
    #7 - EtOH
    z=10
    V = np.array([1,1,1,2,1,4,3])
    Not_H = np.transpose(V*Componentes)
    Componentes=np.array([[1,11.79,0,1.53,0,1,0],
                          [0,0,0,0,0,0,1],
                          [2,13.79,0,1.54,0,1,0],
                          [0,2,1,0,3,0,0]])
    Interation = np.array([[0.9,0.67,0.45,1.12,1,1.68,2.11],
                           [0.85,0.54,0.23,0.87,1.2,1.42,1.97],
                           [0,0,0,74.54,644.60,972.40,3582.81],
                           [0,0,0,74.54,644.60,972.40,3582.81],
                           [0,0,0,74.54,644.60,972.40,3582.81],
                           [292.30,292.30,292.30,0,724.4,-577.50,241.75],
                           [328.2,328.2,328.2,470.7,0,195.6,5299.17],
                           [-320.10,-320.10,-320.10,485.60,180.60,0,-395.51],
                           [-53.92,-53.92,-53.92,-4658.24,-550.58,106.42,0]])
    #Parte configuracional.
    x = np.array([x1,x2,x3,x4])
    r = np.dot(Componentes,np.transpose(Interation[0]))
    q = np.dot(Componentes,np.transpose(Interation[1]))
    l = z*(r-q)/2-(r-1)
    fi = r*x/np.sum(r*x)
    ni = q*x/np.sum(q*x)
    lnGamaC = np.log(fi/x) + z/2 * q*np.log(ni/fi) + l +np.sum(x*l)*fi/x
    
    #Parte residual.
    psi = np.exp(Interation[2:]/T)
    X = np.dot(Not_H,x)/np.sum(np.dot(Not_H,x))
    Xi = Not_H/np.dot(np.transpose(Not_H),np.ones(len(Not_H)))
    theta = Interation[1]*X/np.sum(Interation[1]*X)

    
    #Construção da soma difícil.
    DUMMY1 = theta*psi
    DUMMY2 = np.dot(theta,np.transpose(psi))
    DUMMY3 = DUMMY1/DUMMY2
    lnGAMMA = Interation[1]*(1 - np.log(np.dot(np.transpose(psi),X)) - DUMMY3 )
    
    
    
    
    
    
    
    