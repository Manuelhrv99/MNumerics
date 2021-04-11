# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:14:33 2020

@author: mhrv9
"""


import matplotlib.pyplot as plt
from tabulate import tabulate
from math import *

def euler_comp ():
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
                break
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
    y_m = y
    solve_x = []
    solve_y = []
    solve_u = []
    solve_y_m = []
    solve_x.append(x)
    solve_y.append(y)
    solve_u.append(0)
    solve_y_m.append(y)
    for i in range (0, n):
        u = y + (h*(x + (y/n)))
        expr = eval(f)
                  #Despues del asterisco va la función
        y = y + (h*(expr))
        y_m = y_m + ((h/2)*((expr)+((x+h)+(u/n))))
        x = x + h
        solve_x.append(x)
        solve_y.append(y)
        solve_u.append(u)
        solve_y_m.append(y_m)
    return solve_x, solve_y, solve_u, solve_y_m

def graph (results_x, results_y, results_y_m):
    iteration_num = len(results_x)
    x = ([[None]]*(iteration_num))
    y = ([[None]]*(iteration_num))    
    y_m = ([[None]]*(iteration_num)) 
    for i in range (0, iteration_num):
        x[i] = [results_x[i]]
        y[i] = [results_y[i]]
        y_m[i] = [results_y_m[i]]
    iteration_num = iteration_num - 1
    if x[0] < x[iteration_num] and y[0] < y[iteration_num]:
        x.sort()
        y.sort()
        y_m.sort()
    else:
        if x[0] > x[iteration_num] and y[0] > y[iteration_num]:
            x.sort(reverse=True)
            y.sort(reverse=True)
            y_m.sort(reverse=True)
        else:
            if x[0] > x[iteration_num]:
                x.sort(reverse=True)
                y.sort()
                y_m.sort()
            else:
                if y[0] > y[iteration_num]:
                    x.sort()
                    y.sort(reverse=True)
                    y_m.sort(reverse=True)
    plt.xlabel('Xi')
    plt.ylabel('Yi')
    plt.title('Euler || Azul = Normal || Rojo = Mejorado')
    #Normal
    plt.plot(x, y, c='b')
    #Mejorado
    plt.plot(x, y_m, c='r')
    plt.show()
    
def print_table (results_x, results_y, results_u, results_y_m):
    iteration_num = len(results_x)
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi Normal', 'Yi Normal', 'Xi Mejorado', 'Ui', 'Yi Mejorado']
    for i in range (0, iteration_num):
        table[i] = [i, results_x[i], results_y[i], results_x[i], results_u[i], results_y_m[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    #
    #Calcula e imprime el error entre Euler normal y Euler Mejorado
    #
    error = ((results_y_m[iteration_num-1] - results_y[iteration_num-1]) / results_y_m[iteration_num-1]) * 100
    print ('Resultado')
    print('Error = {:.4f} - {:.4f} / {:.4f} * 100'.format(float(results_y_m[iteration_num-1]), 
                                                          float(results_y[iteration_num-1]), 
                                                          float(results_y_m[iteration_num-1])))
    print('Error = {:.4f}%'.format(abs(error)))

if __name__ == '__main__':
    results_x, results_y, results_u, results_y_m = euler_comp()
    print_table(results_x, results_y, results_u, results_y_m)
    graph(results_x, results_y, results_y_m)