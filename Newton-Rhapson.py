# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 23:02:25 2020

@author: mhrv9
"""


from tabulate import tabulate
from sympy import Symbol
from sympy import cos
from sympy import sin

def calculate():
    #
    #Lee Xo
    #
    while True:
        try:
            Xo = float(input('¿Cuanto vale Xo? '))
            break
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
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
            print("O P C I Ó N   N O   V A L I D A")
    #Lee el error
    while True:
        try:
            print('Ejemplo de error: 1x10-³ --> 0.001')
            error = float(input('Escribe el tamaño del error: '))
            break
        except ValueError:
            print("O P C I Ó N   N O   V A L I D A")
    #Hace las iteraciones
    x = Symbol('x')
    expr = eval(f)
    derived = expr.diff(x)
    print('La derivada de la función es : '+str(derived))
    calc_error = 1
    #
    #Variables para guardar los resultados
    #
    solve_xo = [Xo]
    solve_error = [calc_error-1]
    while calc_error > error:
        x = Xo
        expr = eval(f)
        expr_g = eval(str(derived))
        Xi_1 = Xo - (expr/expr_g)
        calc_error = abs(Xi_1 - Xo)
        Xo = Xi_1
        solve_xo.append(Xo)
        solve_error.append(calc_error)
    return solve_xo, solve_error
    
def print_table(results_xo, results_error):
    n = len(results_xo)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xo', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xo[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print('La raiz de convergencia es: '+str(results_xo[n-1]))

if __name__ == '__main__':
    results_xo, results_error = calculate()
    print_table(results_xo, results_error)