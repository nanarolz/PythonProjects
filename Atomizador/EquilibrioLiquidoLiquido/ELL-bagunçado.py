

import scipy.optimize
import numpy as np

#Utilizando a seguinte notação:
#1 - óleo de Girassol 
#2 - Álcool
#3 - Ester 
#4 - Glicerol
 
def gamma(x,T):
    #Colunas
    #1 - CH3
    #2 - CH2
    #3 - CH
    #4 - CH--CH
    #5 - OH
    #6 - CH2COO
    #7 - EtOH
    z=10
    Componentes=np.array([
                          [0,0,0,0,0,0,1],
                          [2,13.79,0,1.54,0,1,0],
                          [0,0,0,0,0,0,3]])
    
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
    r = np.dot(Componentes,np.transpose(Interation[0]))
    q = np.dot(Componentes,np.transpose(Interation[1]))
    l = z*(r-q)/2-(r-1)
    fi = r*x/np.sum(r*x)
    ni = q*x/np.sum(q*x)
    lnGamaC = np.log(fi/x) + z/2 * q*np.log(ni/fi) + l +np.sum(x*l)*fi/x
    
    #Parte residual.
    psi = np.exp(-Interation[2:]/T)
    X = np.dot(np.transpose(Componentes),x)/np.sum(np.dot(np.transpose(Componentes),x))
    theta = Interation[1]*X/np.sum(Interation[1]*X)
    
    #Construção da soma difícil.
    DUMMY1 = theta*psi
    DUMMY2 = np.dot(theta,psi)
    DUMMY3 = DUMMY1/DUMMY2
    lnGAMMAR1 = Interation[1]*(1 - np.log((theta*psi).sum(axis=1)) - np.sum(DUMMY3,axis=1) )
    
    
    lnGAMMAR2 = []
    for i in range(len(x)):
        x_dummy=np.zeros(len(x))
        x_dummy[i]=1
        X = np.dot(np.transpose(Componentes),x_dummy)/np.sum(np.dot(np.transpose(Componentes),x_dummy))
        theta = Interation[1]*X/np.sum(Interation[1]*X)
    
        #Construção da soma difícil.
        DUMMY1 = theta*psi
        DUMMY2 = np.dot(theta,psi)
        DUMMY3 = DUMMY1/DUMMY2
        lnGAMMAR2.append(Interation[1]*(1 - np.log((theta*psi).sum(axis=1)) - np.sum(DUMMY3,axis=1) ))
    
    lnGAMMAR2=np.array(lnGAMMAR2) 
    lnGAMMAR = np.sum((Componentes*(lnGAMMAR1-lnGAMMAR2)),axis=1)
    
    #Final
    LnGamma = lnGamaC + lnGAMMAR
    return np.exp(LnGamma)

def Equilíbrio(x_global,T,nit = 150):
    #Estimativa do phase split.
    beta = 0.5
    x_phase1 = np.array([0.05,0.05,0.9])
    x_phase2 = (x_global- beta*x_phase1)/(1-beta)
    
    for i in range(nit):
        Gamma_phase1 = gamma(x_phase1,T)
        Gamma_phase2 = gamma(x_phase2,T)
        K=Gamma_phase1/Gamma_phase2
        
        f = lambda beta_new : np.sum(x_global/(beta + K*(1-beta))) - 1
        beta = scipy.optimize.newton(f,beta, maxiter = 200,tol=1e-3)
        
        x_phase1 = x_global/(beta + K*(1-beta))
        x_phase2 = (x_global- beta*x_phase1)/(1-beta)
    
    return np.array([x_phase1,x_phase2])
