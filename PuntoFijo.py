# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 23:48:03 2020

@author: mhrv9
"""


from colorama import init, Fore, Back, Style
from tabulate import tabulate
from sympy import Symbol
from sympy import cos
from sympy import sin
import sys

def static_point():
    #
    #Lee Xo
    #
    while True:
        try:
            Xi = float(input('¿Cuanto vale Xo? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee la función
    #
    while True:
        try:
            print('Simplificar ecuación ejemplo: x³ + 2x² + 10x - 20 = 0 == x = 20 / x³ + 2x +10')
            print('Ejemplo de función simplificada: Coseno X -3X se escribe --> cos(x) / 3')
            print('Ejemplo de función simplicada: x³ + 2x² + 10x - 20 se escribe --> 20 / (x**2 + 2*x +10)')
            f = str(input('Escribe la función simplificada: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Lee el error
    while True:
        try:
            print('Ejemplo de error: 1x10-³ --> 0.0001')
            error = float(input('Escribe el tamaño del error: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    g_xi = 0
    calc_error = 1
    #
    #Variables para guardar los resultados
    #
    solve_xi = [Xi]
    solve_g_xi = [g_xi]
    solve_error = [calc_error-1]
    #Hace las iteraciones
    i = 1
    while calc_error > error:
        if i <= 40:
            x = Xi
            expr = eval(f)
            g_xi = expr
            calc_error = abs(g_xi - Xi)
            solve_xi.append(Xi)
            Xi = g_xi
            solve_g_xi.append(g_xi)
            solve_error.append(calc_error)
            i = i+1
        else:
            print(Fore.WHITE +'El problema no tiene solución')
            sys.exit()
    return solve_xi, solve_g_xi, solve_error
    
def print_table(results_xi, results_g_xi, results_error):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'g(Xi)', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_g_xi[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xi[n-1]))

if __name__ == '__main__':
    results_xi, results_g_xi, results_error = static_point()
    print_table(results_xi, results_g_xi, results_error)