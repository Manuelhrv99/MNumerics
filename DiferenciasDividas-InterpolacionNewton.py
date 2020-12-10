# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:49:14 2020

@author: mhrv9
"""


from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def run ():
    #Leer Xi del usuario
    #Los while validan que el usuario escriba un valor correcto
    while True:
        try:
            iteration_num = int(input('¿Cuantas iteraciones vas a calcular? '))
            break
        except ValueError:
            print('Escribe un numero')
    print('Introduce los valores de Xi')
    Xi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                Xi[i] = float(input('Xi en la posición {}: '.format(i)))
                break
            except ValueError:
                print('Escribe un numero')
    #Leer f(Xi) del usuario
    print('Introduce los valores de f(Xi)')
    fXi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                fXi[i]=float(input('f(Xi) en la posición {}: '.format(i)))
                break
            except ValueError:
                print('Escribe un numero')
    #Lee la posicion de X que busca el usuario
    while True:
        try:
            question = str(input('¿Deseas calcular algún valor? || Si/No '))
            break
        except ValueError:
            print('Respuesta invalida')
    #Variables inicializadas
    work = False
    user_xi = 0
    result = 0
    if question.upper() == 'SI':
        while True:
            try:
                user_xi = float (input('¿Qué valor deseas calcular? '))
                break
            except ValueError:
                print('Escribe un numero')
        #Con resultado
        work = True
        #Aqui va el resultado
        result = calculate(Xi, fXi, user_xi, work)
        graph (Xi, fXi, user_xi, result, iteration_num, work)
        print ('El resultado de f(Xi) en el punto Xi = {:.2f} es de {:.4f}'.format(user_xi, result))
    else:
        #Sin resultado
        graph (Xi, fXi, user_xi, result, iteration_num, work)
    #Crea el polinomio en formato legible
    polynomial = lagrange(Xi, fXi)
    print ('Polinomio')
    print (polynomial)
    print_table (Xi, fXi)
    
def calculate (Xi, fXi, user_xi, work):
    array_lenght = len(Xi)
    fill = np.zeros(array_lenght)
    divided_difference = np.zeros((array_lenght-1, array_lenght-1))
    fill[0] = fXi[0]
    for i in range (0, array_lenght-1):
        divided_difference[i,0] = (fXi[i+1] - fXi[i]) / (Xi[i+1] - Xi[i])
        
    for j in range (1, array_lenght-1):
        for i in range (0, array_lenght-j-1):
            divided_difference[i,j] = (divided_difference[i+1, j-1] - divided_difference[i, j-1]) / (Xi[j+i+1] - Xi[i])
      
    for i in range (1, array_lenght):
        fill[i] = divided_difference[0, i-1]
        
    if work == True:
        newton_result = fill[0]
        product_Xi = 1
        for i in range (1, array_lenght):
            product_Xi = product_Xi * (user_xi - Xi[i-1])
            newton_result += fill[i] * product_Xi
    
        return newton_result

def print_table (Xi, fXi):
    #Tabla de Diferencias Divididas Avanzadas
    headers = ['Iteraciones','Xi','f(Xi)']
    n = len(Xi)
    ki = np.arange(0,n,1)
    table = np.concatenate(([ki],[Xi],[fXi]),axis=0)
    table = np.transpose(table)
    #Diferencias divididas vacia
    d_fin = np.zeros(shape=(n,n),dtype=float)
    table = np.concatenate((table, d_fin), axis=1)
    #Calcula tabla, inicia en columna 3
    [n,m] = np.shape(table)
    slash = n-1
    j = 3
    while (j < m):
        #Añade título para cada columna
        headers.append('F['+str(j-2)+']')
        #Cada fila de columna
        i = 0
        # inicia en 1
        step = j-2
        while (i < slash):
            denominator = (Xi[i+step]-Xi[i])
            numerator = table[i+1,j-1]-table[i,j-1]
            table[i,j] = numerator/denominator
            i = i+1
        slash = slash - 1
        j = j+1
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    
def graph (Xi, fXi, user_xi, result, iteration_num, work):
    if work == True:
        x = ([[None]]*(iteration_num+1))
        y = ([[None]]*(iteration_num+1))
        for i in range (0, iteration_num):
            x[i] = [Xi[i]]
            y[i] = [fXi[i]]
        x[iteration_num] = [user_xi]
        y[iteration_num] = [result]
        plt.axvline(user_xi, color='r')
        plt.axhline(result, color='r',)
    else:
        x = ([[None]]*(iteration_num))
        y = ([[None]]*(iteration_num))      
        for i in range (0, iteration_num):
            x[i] = [Xi[i]]
            y[i] = [fXi[i]]
    iteration_num = iteration_num - 1
    if x[0] < x[iteration_num] and y[0] < y[iteration_num]:
        x.sort()
        y.sort()
    else:
        if x[0] > x[iteration_num] and y[0] > y[iteration_num]:
            x.sort(reverse=True)
            y.sort(reverse=True)
        else:
            if x[0] > x[iteration_num]:
                x.sort(reverse=True)
                y.sort()
            else:
                if y[0] > y[iteration_num]:
                    x.sort()
                    y.sort(reverse=True)

    plt.plot(x, y, '-o', c='b')
    plt.xlabel('Xi')
    plt.ylabel('f(Xi)')
    plt.title('Diferencias Divididas')

if __name__ == '__main__':
    run ()
"""Xi=numpy.array([1, 5, 20, 40])
fXi=numpy.array([56.5, 113.0, 181.0, 214.5])"""