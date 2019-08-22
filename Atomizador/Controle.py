
import numpy

# CONTROLE DA TEMPERATURA

Kcp = 3.03
kc1 = 36.629
tau_i = 4024

# eu forneco o set point - SP
erro = SP - tempreator # calcula o erro
soma = soma + (erro + erro_anterior)
contador_condensador = contador_condensador + 1

if erro > 0:
    R = Kcp * erro

    if R < 0: # resistencia menor que 0%
        R = 0
    
    if R > 100: # resistencia maior que 100%
        R = 100

    R = str(R) # convertendo para string
    R = 'R' + R # adicionando caractere

    conexao.write(bytes(R, 'UTF-8'))
    time.sleep(1)

else:
    # condensador    
    conexao.write(b'R000')
    time.sleep(1)

    C = Kc1 * ( abs(erro) + (1 / tau_i) * soma )

    if C < 0: 
        C = 0
    
    if C > 100:
        C = 100

    if(contador_condensador > 120): # passado 120 segundos
        
        contador_condensador = 0

        C = str(C) # convertendo para string
        C = 'j' + C # adicionando caractere

        conexao.write(bytes(C, 'UTF-8'))

erro_anterior = erro