# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:51:41 2020

@author: mhrv9
"""


import matplotlib.pyplot as plt
from tabulate import tabulate
from math import *
import math

def runge_4 ():
    #
    #Lee x(0) y x(1)
    #
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                x = float(input('¿Cuanto vale x(0)? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                x_final = float(input('¿Cuanto vale x(final)? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #
    #Lee y(0)
    #
    while True:
            try:
                y = float(input('¿Cuanto vale y(0)? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #
    #Pregunta si se conoce el valor de n o h
    #
    while True:
        try:
            question = str(input('¿Conoces n o h? Escribe n || h: '))
            if question.upper() in ['N', 'H']:
                break
            else:
                print("O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
    #
    #Cuando la respuesta es n
    #
    if (question == 'n'):
        while True:
            try:
                n = int(input('¿Cuantos subintervalos va a calcular? '))
                if n > 0:
                    break
                else:
                    print("O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
        h = float((x_final - x) / n)
    #
    #Cuando la respuesta es h
    #
    else:
        while True:
            try:
                h = float(input('¿Cuanto vale el intervalo? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
        n = int((x_final - x) / h)
    #
    #Lee la función
    #
    while True:
        try:
            print('Ejemplo de función: √y/2x+1 se escribe --> sqrt(y)/((2*x)+1)')
            f = str(input('Escribe la función: '))
            break
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
    #
    #Hace las iteraciones
    #
    #f = x-y
    solve_x = []
    solve_y = []
    solve_x.append(x)
    solve_y.append(y)
    for i in range (0, n):
        if y == 0:
            y = 1
            expr = eval(f)
            expr = expr - 1
        else:
            expr = eval(f)
        k_1 = expr
        k_2 = ((x + 0.5*h) - (y + 0.5*k_1*h))
        k_3 = ((x + 0.5*h) - (y + 0.5*k_2*h))
        k_4 = ((x + h) - (y + k_3*h))
        y = y + (1.0/6.0)*(k_1 + 2*k_2 + 2*k_3 + k_4)*h
        x = x + h
        solve_x.append(x)
        solve_y.append(y)
    return solve_x, solve_y

def graph (results_x, results_y):
    iteration_num = len(results_x)
    x = ([[None]]*(iteration_num))
    y = ([[None]]*(iteration_num))
    for i in range (0, iteration_num):
        x[i] = [results_x[i]]
        y[i] = [results_y[i]]
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
    plt.xlabel('Xi')
    plt.ylabel('Yi')
    plt.title('Runge - Kutta 4° orden')
    plt.plot(x, y, c='b')
    plt.show()
    
def print_table (results_x, results_y):
    iteration_num = len(results_x)
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi 2o Orden', 'Yi 2o Orden']
    for i in range (0, iteration_num):
        table[i] = [i, results_x[i], results_y[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    res = results_y[iteration_num-1]
    print('Resultado de y(?) = '+str(res))

if __name__ == '__main__':
    results_x, results_y = runge_4 ()
    print_table(results_x, results_y)
    graph(results_x, results_y)