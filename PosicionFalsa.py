# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:54:32 2020

@author: mhrv9
"""


from colorama import init, Fore, Back, Style
import matplotlib.pyplot as plt
from tabulate import tabulate
import sys

def fake_position():
    #
    #Lee los 4 puntos
    #
    while True:
        try:
            point_1 = float(input('¿Cuanto vale el primer punto? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
        try:
            point_2 = float(input('¿Cuanto vale el segundo punto? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
        try:
            point_3 = float(input('¿Cuanto vale el tercer punto? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
        try:
            point_4 = float(input('¿Cuanto vale el cuarto punto? '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee la función
    #
    while True:
        try:
            print('Ejemplo de función: x³ + 2x² + 10x - 20 se escribe --> x**3+2*x**2+10*x-20')
            f = str(input('Escribe la función: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Se calcula si tiene cambio de signo
    x = point_1
    expr = eval(f)
    res_1 = expr
    
    x = point_2
    expr = eval(f)
    res_2 = expr
    
    x = point_3
    expr = eval(f)
    res_3 = expr
    
    x = point_4
    expr = eval(f)
    res_4 = expr
    if res_1 < 0 and res_2 > 0:
        Xi = point_1
        Xd = point_2
        f_xi = res_1
        f_xd = res_2
    else:
        if res_2 < 0 and res_3 > 0:
            Xi = point_2
            Xd = point_3
            f_xi = res_2
            f_xd = res_3
        else:
            if res_3 < 0 and res_4 > 0:
                Xi = point_3
                Xd = point_4
                f_xi = res_3
                f_xd = res_4
            else:
                print(Fore.WHITE +'No tiene solución')
                sys.exit() #Corta el programa
    #Lee la respuesta si es error o iteraciones
    while True:
        try:
            question = str(input('¿Quieres calcular un minimo de Error o de Iteraciones? || E || I '))
            if question.upper() in ['E', 'I']:
                break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Variables para guardar los resultados
    #
    calc_error = 1
    Xm = 0
    f_xm = 0
    solve_xi = [Xi]
    solve_xd = [Xd]
    solve_xm = [Xm]
    solve_f_xm = [f_xm]
    #Cuando es error
    if question.upper() == 'E':
        while True:
            try:
                print('Ejemplo de error: 1x10-³ --> 0.001')
                error = float(input('Escribe el tamaño del error: '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        #Hace las iteraciones
        while calc_error > error:
            Xm = Xd - (((Xd - Xi)*f_xd) / (f_xd - f_xi))
            x = Xm
            expr = eval(f)
            f_xm = abs(expr)
            Xi = Xm
            x = Xi
            expr = eval(f)
            f_xi = expr
            solve_xi.append(Xi)
            solve_xd.append(Xd)
            solve_xm.append(Xm)
            solve_f_xm.append(f_xm)
    #Cuando es por iteraciones
    else:
        while True:
            try:
                n = int(input('¿Cuantas iteraciones vas a calcular? '))
                if n > 0:
                    break
                else:
                    print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        #Hace las iteraciones
        for i in range (0, n):
            Xm = Xd - (((Xd - Xi)*f_xd) / (f_xd - f_xi))
            x = Xm
            expr = eval(f)
            f_xm = abs(expr)
            Xi = Xm
            x = Xi
            expr = eval(f)
            f_xi = expr
            solve_xi.append(Xi)
            solve_xd.append(Xd)
            solve_xm.append(Xm)
            solve_f_xm.append(f_xm)
    return solve_xi, solve_xd, solve_xm, solve_f_xm
    
def print_table(results_xi, results_xd, results_xm, results_f_xm):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'Xd', 'Xm', '|f(Xm)|']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_xd[i], results_xm[i], results_f_xm[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xm[n-1]))
    
def graph (results_xi, results_xd):
    iteration_num = len(results_xi)
    x = ([[None]]*(iteration_num))
    y = ([[None]]*(iteration_num))      
    for i in range (0, iteration_num):
        x[i] = [results_xi[i]]
        y[i] = [results_xd[i]]
    plt.plot(x, y, '-o', c='b')
    plt.xlabel('Xi')
    plt.ylabel('Xd')
    plt.title('Posición Falsa')

if __name__ == '__main__':
    results_xi, results_xd, results_xm, results_f_xm = fake_position()
    print_table(results_xi, results_xd, results_xm, results_f_xm)
    graph(results_xi, results_xd)