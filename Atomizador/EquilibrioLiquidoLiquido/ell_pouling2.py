
import numpy as np
import scipy.optimize 

T = 307
x1 = 0.047
x2 = 1 - x1
x = np.array([x1,x2])
z = 10

#                       [ CH3 , CH3CO , CH2 ]
Componentes = np.array([[   1 ,     1 ,   0 ], # acetona
                        [   2 ,     0 ,   3 ]]) # n-pentano

#    [ CH3   ,  CH3CO ,    CH2 ]
Rx = [0.6325 , 1.7048 , 0.6325 ]
Qx = [1.0608 , 1.6700 , 0.7081 ]

#             [ CH3   ,  CH3CO ,    CH2 ] 
a = np.array([[0.0000 , 433.60 ,  0.000 ], #CH3
              [199.00 , 0.0000 , 199.00 ], #CH3CO
              [0.0000 , 433.60 ,  0.000 ]]) #CH2
#             [ CH3   ,  CH3CO ,    CH2 ] 
b = np.array([[ 0.0000 , 0.1473 ,   0.000 ], #CH3
              [-0.8709 , 0.0000 , -0.8709 ], #CH3CO
              [ 0.0000 , 0.1473 ,   0.000 ]]) #CH2
#             [ CH3   ,  CH3CO ,    CH2 ] 
c = np.array([[0.0000 , 0.0000 ,  0.000 ], #CH3
              [0.0000 , 0.0000 , 0.0000 ], #CH3CO
              [0.0000 , 0.0000 ,  0.000 ]]) #CH2

 #-----------------------------------------------------------CONFIGURACIONAL
r = np.dot(Componentes,np.transpose(Rx))
q = np.dot(Componentes,np.transpose(Qx))
l = z*(r-q)/2-(r-1)
fi = r*(x**(3/4))/np.sum(r*(x**(3/4)))
ni = q*x/np.sum(q*x)
lnGamaC = np.log(fi/x) + z/2*q*np.log(ni/fi) + l - np.sum(x*l)*fi/x

#------------------------------------------------------------------RESIDUAL
psi = np.exp(-((a + b*T + c*(T**2))/T))

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