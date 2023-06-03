# -*- coding: utf-8 -*-
"""
Created on Sat May  6 14:15:02 2023

@author: eliel
"""

import numpy as np
from scipy import optimize, linalg
import matplotlib.pyplot as plt


'''
Essa função serve para construir o gráfico "exato"
'''
def funcaodeajuste(t, a, v0, x0, noise=0., n_outliers=0, seed=None):

    x = a*t**2/2+v0*t+x0
    #v=a*t+v0
    #ac = a
    return x

'''
Essa função serve para calcular o resíduo (erro)

def residuo(parametros, t, x):
# O parametro tem a mesma estrutura do vetor parametros_iniciais    
#    print(parametros)
    
    return parametros[0]*t**2/2+parametros[1]*t+parametros[2] - x
'''

'''
A equação acima é o mesmo que:
a*t²/2+v0*t+x0
onde x é o ponto experimental

'''


'''
Aqui são os parametros iniciais da função:
    a*t**2/2+vo*t+x0
'''
a = 50.
v0 = 1.
x0 = 0.1


parametros_iniciais = np.array([a, v0, x0])

'''
parametros de referência
'''
ai = 9.81
v0i =0
x0i = 0.1   

parametros_referencia = np.array([ai, v0i, x0i])


'''
Limitador dos parâmetros, caso preciso, depende do método.
'''
Limites=([0,-20,0.000],[100,20,0.3])


'''
Importação dos dados medidos
'''

dados=np.loadtxt('dados2.txt',delimiter='\t')
tempos = 2*dados[:,0]
deslocamentos = dados[:,1]



'''
Código para a otimização dos parâmetros
'''
popt, pcov = optimize.curve_fit(funcaodeajuste, tempos, deslocamentos, bounds=Limites)

'''
res_lsq = optimize.least_squares(residuo, parametros_iniciais, jac='2-point',
                        args=(tempos, deslocamentos),bounds=Limites)
'''
'''
O resultado dos parâmetros otimizados é encontrado em res_lsq.x
'''
Parametrosotimizados=popt

'''
Calculo dos desvios dos parametros
'''

perr = np.sqrt(np.diag(pcov))

'''
Preparando os dados para realizar o gráfico da curva ajustada
'''
t_min = min(tempos)
t_max = max(tempos)
n_points = 150

'''
t_grid serve para espaçar regularmente os n_points entre t_min e t_max
'''

t_grid = np.linspace(t_min, t_max, n_points)

'''
y_lsq representa os valores de y para a curva de ajuste otimizada.
'''
y_lsq = funcaodeajuste(t_grid, *Parametrosotimizados)

'''
y_ideal é a curva com os parâmetros de ajuste "corretos"
'''

y_ideal = funcaodeajuste(t_grid, *parametros_referencia)


'''
Plot dos pontos (dados orinigais)

'''
plt.plot(tempos, deslocamentos, 'o', label="dados")

'''
Plot da curva de ajuste
'''

plt.plot(t_grid, y_lsq, label='ajuste')

'''
Plot da curva "esperada" (teoria)
'''

plt.plot(t_grid, y_ideal, label='esperado')

'''
Nomeando os eixos
'''
plt.xlabel("tempo (s)")

plt.ylabel("deslocamento (m)")

plt.legend()

'''
Cria o gráfico
'''
plt.show()


