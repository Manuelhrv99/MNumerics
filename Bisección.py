# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:57:58 2020

@author: mhrv9
"""


import matplotlib.pyplot as plt
from tabulate import tabulate
from sympy import *
import math
import sys

def bisection ():
    #
    #Lee Xi y XD
    #
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                Xi = int(input('¿Cuanto vale Xi? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                Xd = int(input('¿Cuanto vale Xd? '))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #
    #Lee la función
    #
    while True:
        try:#x**3-6*x**2+11*x-6
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
    x = Xi
    expr = eval(f)
    fXi = expr
    x = Xd
    expr = eval(f)
    fXd = expr
    if fXi < 0 and fXd > 0:
        #
        #Calcular n
        #
        n = (math.log(Xd-Xi, math.e) - math.log(error, math.e)) / math.log(2, math.e)
        n = round(n)
        #Guardan los resultados
        solve_xi = ([[None]]*(n+1))
        solve_xd = ([[None]]*(n+1))
        solve_fxi = ([[None]]*(n+1))
        solve_fxd = ([[None]]*(n+1))
        solve_xi[0] = Xi
        solve_xd[0] = Xd
        solve_fxi[0] = fXi
        solve_fxd[0] = fXd
        #Guardan los resultados
        Xm = 0
        Xm_aux = 0
        calc_error = Xm - Xm_aux
        print('El problema tiene solucion')
        table = ([[None]]*(n+1))
        headers = ['Iteraciones', 'Xi', 'Xd', 'f(Xi)', 'f(Xd)', 'Xm', 'Error']
        table[0] = [0, Xi, Xd, fXi, fXd, Xm, abs(calc_error)]
        for i in range (0, n):
            Xm_aux = Xm
            Xm = (Xi + Xd) / 2
            calc_error = Xm - Xm_aux
            x = Xm #Se actualiza el valor de x adentro de la funcion
            expr = eval(f)
            f_aux = expr
            if f_aux > 0:
                #Cuando se altera Xd
                Xd = Xm
                fXd = f_aux
                #Xi se mantiene igual
                Xi = Xi
                fXi = fXi
            else:
                #Cuando se altera Xi
                Xi = Xm
                fXi = f_aux
                #Xd se mantiene igual
                Xd = Xd
                fXd = fXd
            table[i+1] = [i+1, Xi, Xd, fXi, fXd, Xm, abs(calc_error)]
            solve_xi[i+1] = Xi
            solve_xd[i+1] = Xd
            solve_fxi[i+1] = fXi
            solve_fxd[i+1] = fXd
    else:
        print('El problema NO tiene solucion')
        sys.exit() #Corta el programa
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print('La raiz de solucion es = '+str(Xm))
    return solve_xi, solve_xd, solve_fxi, solve_fxd
    

def graph (results_xi, results_xd, results_fxi, results_fxd):
    iteration_num = len(results_xi)
    iteration_num = iteration_num - 1
    if results_xi[0] < results_xi[iteration_num] and results_xd[0] < results_xd[iteration_num]:
        results_xi.sort()
        results_xd.sort()
        results_fxi.sort()
        results_fxd.sort()
    else:
        if results_xi[0] > results_xi[iteration_num] and results_xd[0] > results_xd[iteration_num]:
            results_xi.sort(reverse=True)
            results_xd.sort(reverse=True)
            results_fxi.sort(reverse=True)
            results_fxd.sort(reverse=True)
        else:
            if results_xi[0] > results_xi[iteration_num]:
                results_xi.sort(reverse=True)
                results_xd.sort()
                results_fxi.sort(reverse=True)
                results_fxd.sort()
            else:
                if results_xd[0] > results_xd[iteration_num]:
                    results_xi.sort()
                    results_xd.sort(reverse=True)
                    results_fxi.sort()
                    results_fxd.sort(reverse=True)
    fig1 = plt.figure("Xi y Xd")
    fig1.subplots_adjust(hspace=0.5, wspace=0.5)
    for i in range(1, 2):
        ax = fig1.add_subplot(1, 1, i)
        ax.set_xlabel("Xi")
        ax.set_ylabel("Xd")
        ax.set_title('Bisección')
        ax.plot(results_xi, results_xd,"-o", c="b")
    fig2 = plt.figure("f(Xi) y f(Xd)")
    fig2.subplots_adjust(hspace=0.5, wspace=0.5)
    for i in range(1, 2):
        ax = fig2.add_subplot(1, 1, i)
        ax.set_xlabel("f(Xi)")
        ax.set_ylabel("f(Xd)")
        ax.set_title('Bisección')
        ax.plot(results_fxi, results_fxd,"-o", c="b")

if __name__ == '__main__':
    results_xi, results_xd, results_fxi, results_fxd = bisection()
    graph(results_xi, results_xd, results_fxi, results_fxd)