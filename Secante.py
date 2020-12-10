# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 23:09:22 2020

@author: mhrv9
"""


from colorama import init, Fore, Back, Style
from tabulate import tabulate
from sympy import Symbol
from sympy import cos
from sympy import sin

def secant():
    #
    #Lee X(0) y X(1)
    #
    while True:
        try:
            x_0 = float(input('¿Cuanto vale X(0)? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
        try:
            x_1 = float(input('¿Cuanto vale X(1)? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee la función
    #
    while True:
        try:
            print('Ejemplo de función: Coseno X-X se escribe --> cos(x)-x')
            print('Ejemplo de función: x³ + 2x² + 10x - 20 se escribe --> x**3+2*x**2+10*x-20')
            f = str(input('Escribe la función: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Lee el error
    while True:
        try:
            print('Ejemplo de error: 1x10-³ --> 0.001')
            error = float(input('Escribe el tamaño del error: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Variables para guardar los resultados
    #
    calc_error = 1
    solve_xi = [x_0]
    solve_error = [calc_error-1]
    #Hace las iteraciones
    while calc_error > error:
        x = x_1
        expr = eval(f)
        f_x1 = expr
        x = x_0
        expr = eval(f)
        f_x0 = expr
        aux_xi = x_1 - ((x_1 - x_0)*(f_x1) / (f_x1 - f_x0))
        calc_error = abs(x_1 - x_0)
        x_0 = x_1
        x_1 = aux_xi
        solve_xi.append(x_0)
        solve_error.append(calc_error)
    return solve_xi, solve_error
    
def print_table(results_xi, results_error):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xi[n-1]))

if __name__ == '__main__':
    results_xi, results_error = secant()
    print_table(results_xi, results_error)