# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:25:04 2020

@author: mhrv9
"""


from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def lagrangeMethod ():
    #Leer Xi del usuario
    #Los while validan que el usuario escriba un valor correcto
    while True:
        try:
            iteration_num = int(input('¿Cuantas iteraciones vas a calcular? '))
            if iteration_num > 0:
                break
            else:
                print("O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
    print('Introduce los valores de Xi')
    Xi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                Xi[i] = float(input('Xi en la posición {}: '.format(i)))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #Leer f(Xi) del usuario
    print('Introduce los valores de f(Xi)')
    fXi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                fXi[i]=float(input('f(Xi) en la posición {}: '.format(i)))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #Lee la posicion de X que busca el usuario
    while True:
        try:
            question = str(input('¿Deseas calcular algún valor? || Si/No '))
            break
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
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
                print("O P C I Ó N   N O   V A L I D A")
        #Con resultado
        work = True
        #Aqui va el resultado
        result = calculate(Xi, fXi, user_xi)
        graph (Xi, fXi, user_xi, result, iteration_num, work)
        print ('El resultado de f(Xi) en el punto Xi = {:.2f} es de {:.4f}'.format(user_xi, result))
    else:
        #Sin resultado
        graph (Xi, fXi, user_xi, result, iteration_num, work)
    #Crea el polinomio en formato legible
    polynomial = lagrange(Xi, fXi)
    print ('Polinomio')
    print (polynomial)
    print_table (Xi, fXi, iteration_num)

def calculate (Xi, fXi, user_xi):      
    polynomial = lagrange(Xi, fXi)
    print ('Polinomio')
    print (polynomial)
    lag_result = polynomial(user_xi)
    print (lag_result)
    return lag_result

def print_table (Xi, fXi, iteration_num):
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi', 'f(Xi)']
    for i in range (0, iteration_num):
        table[i] = [i, Xi[i], fXi[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid'))
    
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
    lagrangeMethod ()