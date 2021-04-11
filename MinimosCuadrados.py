# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:54:37 2020

@author: mhrv9
"""


import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def minimum_squares ():
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
    Xi=np.array([0.00]*iteration_num, dtype=np.complex_)
    for i in range (0, iteration_num):
        while True:
            try:
                Xi[i] = complex(input('Xi en la posición {}: '.format(i)))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    #Leer f(Xi) del usuario
    print('Introduce los valores de f(Xi)')
    fXi=np.array([0.00]*iteration_num, dtype=np.complex_)
    for i in range (0, iteration_num):
        while True:
            try:
                fXi[i]=complex(input('f(Xi) en la posición {}: '.format(i)))
                break
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
    polynomial_grade, coef_0, coef_1 = calculate(Xi, fXi)
    graph (Xi, fXi, iteration_num, polynomial_grade, coef_0, coef_1)
    
def graph (Xi, fXi, iteration_num, polynomial_grade, coef_0, coef_1):
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
    plt.xlabel('Xi')
    plt.ylabel('f(Xi)')
    plt.title('Minimos Cuadrados')
    if polynomial_grade == 1:
        plt.scatter(Xi, fXi)
        x_g = np.array([min(Xi), max(Xi)])
        fun = coef_1 * x_g + coef_0
        plt.plot(x_g, fun)
        plt.show()
    else:
        plt.plot(x, y, '-o', c='b')  

def calculate (Xi, fXi):
    x = np.asarray(Xi)
    y = np.asarray(fXi)
    #Variables que se usan en minimos cuadrados
    n_x = len(x)
    s_xi = np.sum(x)
    s_fxi = np.sum(y)
    s_fxi_xi = np.sum(x*y)
    s_xi2 = np.sum(x**2)
    s_xi3 = np.sum(x**3)
    s_xi4 = np.sum(x**4)
    s_fxi_xi2 = np.sum((x**2)*y)
    s_xi5 = np.sum(x**5)
    s_xi6 = np.sum(x**6)
    s_fxi_xi3 = np.sum((x**3)*y)
    
    while True:
            try:
                polynomial_size = int(input('¿De qué tamaño va a ser el polinomio? 1 || 2 || 3: '))
                if polynomial_size in [1, 2, 3]:
                    break
                else:
                    print("O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print("O P C I Ó N   N O   V A L I D A")
                
    table = ([[None]]*(n_x+1)) 
    #
    #        
    #Polinomio de grado 1, se usa una ecuacion
    #
    #
    if polynomial_size == 1:
        a_1 = (n_x*s_fxi_xi - s_xi*s_fxi)/(n_x*s_xi2 - s_xi**2)
        a_0 = (s_xi2*s_fxi - s_fxi_xi*s_xi)/(n_x*s_xi2 - s_xi**2)
        headers = ['Iteraciones', 'Xi', 'f(Xi)', 'Xi^2', 'f(Xi)Xi']
        for i in range (0, n_x):
            #
            #Asignacion de los valores en la tabla
            #
            table[i] = [abs(i+1), abs(Xi[i]), abs(fXi[i]), '{:.2e}'.format(abs(Xi[i]**2)), '{:.2e}'.format(abs(fXi[i]*Xi[i]))]
        #
        #Se agregan las sumatorias
        #
        table[n_x] = ('m='+str(n_x), 'Σ={:.2e}'.format(abs(s_xi)), 'Σ={:.2e}'.format(abs(s_fxi)), 
                      'Σ={:.2e}'.format(abs(s_xi2)), 'Σ={:.2e}'.format(abs(s_fxi_xi)))
        print (tabulate(table, headers, tablefmt='fancy_grid')) 
            #
            #Asignacion de los valores en la tabla
            #
        print('Polinomio de grado 1')
        print('{:.4f} + {:.4f}x'.format(abs(a_0), abs(a_1)))
        return polynomial_size, a_0, a_1
    #
    #
    #Polininomios de grados 2, sistemas de ecuaciones
    #
    #Donde a, b y c son la matriz para resolver el sistema 3*3
    elif polynomial_size == 2:        
        a = np.array([[n_x, s_xi, s_xi2], [s_xi, s_xi2, s_xi3], [s_xi2, s_xi3, s_xi4]])
        b = np.array([[s_fxi], [s_fxi_xi], [s_fxi_xi2]])
        c = np.linalg.solve(a,b)
        a_0 = complex(c[0])
        a_1 = complex(c[1])
        a_2 = complex(c[2])
        headers = ['Iteraciones', 'Xi', 'f(Xi)', 'Xi^2', 'f(Xi)Xi', 'Xi^3', 'Xi^4', 'f(Xi)Xi^2']
        for i in range (0, n_x):
            #
            #Asignacion de los valores en la tabla
            #
            table[i] = [abs(i+1), abs(Xi[i]), abs(fXi[i]), '{:.2e}'.format(abs(Xi[i]**2)), '{:.2e}'.format(abs(fXi[i]*Xi[i])), 
                        '{:.2e}'.format(abs(Xi[i]**3)), '{:.2e}'.format(abs(Xi[i]**4)), '{:.2e}'.format(abs(fXi[i]*(Xi[i]**2)))]
        #
        #Se agregan las sumatorias
        #
        table[n_x] = ('m='+str(n_x), 'Σ={:.2e}'.format(abs(s_xi)), 'Σ={:.2e}'.format(abs(s_fxi)), 
                      'Σ={:.2e}'.format(abs(s_xi2)), 'Σ={:.2e}'.format(abs(s_fxi_xi)),
                      'Σ={:.2e}'.format(abs(s_xi3)), 'Σ={:.2e}'.format(abs(s_xi4)), 'Σ={:.2e}'.format(abs(s_fxi_xi2)))
        print (tabulate(table, headers, tablefmt='fancy_grid')) 
            #
            #Asignacion de los valores en la tabla
            #
        #
        #Imprimir de forma visual el sistema de ecuaciones
        #
        print('{} a0 + {:.2f} a1 + {:.2f} a2 = {:.4f}'.format(abs(n_x), abs(s_xi), abs(s_xi2), abs(s_fxi)))
        print('{:.2f} a0 + {:.2f} a1 + {:.2f} a2 = {:.4f}'.format(abs(s_xi), abs(s_xi2), abs(s_xi3), abs(s_fxi_xi)))
        print('{:.2f} a0 + {:.2f} a1 + {:.2f} a2 = {:.4f}'.format(abs(s_xi2), abs(s_xi3), abs(s_xi4), abs(s_fxi_xi2)))
        print('')
        print('a0 = '+str(abs(a_0)))
        print('a1 = '+str(abs(a_1)))
        print('a2 = '+str(abs(a_2)))
        print('')
        print('Polinomio de grado 2')
        print ('{:.4f} + {:.4f}x + {:.4f}x^2'.format(abs(a_0), abs(a_1), abs(a_2)))
        return polynomial_size, a_0, a_1
    #
    #
    #Polininomios de grados 3, sistemas de ecuaciones
    #
    #Donde a, b y c son la matriz para resolver el sistema 4*4
    elif polynomial_size == 3:
        a = np.array([[n_x, s_xi, s_xi2, s_xi3], [s_xi, s_xi2, s_xi3, s_xi4], 
                      [s_xi2, s_xi3, s_xi4, s_xi5], [s_xi3, s_xi4, s_xi5, s_xi6]])
        b = np.array([[s_fxi], [s_fxi_xi], [s_fxi_xi2], [s_fxi_xi3]])      
        c = np.linalg.solve(a,b)
        a_0 = complex(c[0])
        a_1 = complex(c[1])
        a_2 = complex(c[2])
        a_3 = complex(c[3])
        headers = ['Iteraciones', 'Xi', 'f(Xi)', 'Xi^2', 'f(Xi)Xi', 'Xi^3', 'Xi^4', 'f(Xi)Xi^2',
                   'Xi^5', 'Xi^6', 'f(Xi)Xi^3']
        for i in range (0, n_x):
            #
            #Asignacion de los valores en la tabla
            #
            table[i] = [abs(i+1), abs(Xi[i]), abs(fXi[i]), '{:.2e}'.format(abs(Xi[i]**2)), '{:.2e}'.format(abs(fXi[i]*Xi[i])), 
                        '{:.2e}'.format(abs(Xi[i]**3)), '{:.2e}'.format(abs(Xi[i]**4)), '{:.2e}'.format(abs(fXi[i]*(Xi[i]**2))), 
                        '{:.2e}'.format(abs(Xi[i]**5)), '{:.2e}'.format(abs(Xi[i]**6)), '{:.2e}'.format(abs(fXi[i]*(Xi[i]**3)))]
        #
        #Se agregan las sumatorias
        #
        table[n_x] = ('m='+str(n_x), 'Σ={:.2e}'.format(abs(s_xi)), 'Σ={:.2e}'.format(abs(s_fxi)), 
                      'Σ={:.2e}'.format(abs(s_xi2)), 'Σ={:.2e}'.format(abs(s_fxi_xi)),
                      'Σ={:.2e}'.format(abs(s_xi3)), 'Σ={:.2e}'.format(abs(s_xi4)), 'Σ={:.2e}'.format(abs(s_fxi_xi2)),
                      'Σ={:.2e}'.format(abs(s_xi5)), 'Σ={:.2e}'.format(abs(s_xi6)), 'Σ={:.2e}'.format(abs(s_fxi_xi3)))
        print (tabulate(table, headers, tablefmt='fancy_grid'))
            #
            #Asignacion de los valores en la tabla
            #
        #
        #Imprimir de forma visual el sistema de ecuaciones
        #
        print('{} a0 + {:.2f} a1 + {:.2f} a2 + {:.2f} a3 = {:.4f}'.format(abs(n_x), abs(s_xi), abs(s_xi2), abs(s_xi3), abs(s_fxi)))
        print('{:.2f} a0 + {:.2f} a1 + {:.2f} a2 + {:.2f} a3 = {:.4f}'.format(abs(s_xi), abs(s_xi2), abs(s_xi3), abs(s_xi4), abs(s_fxi_xi)))
        print('{:.2f} a0 + {:.2f} a1 + {:.2f} a2 + {:.2f} a3 = {:.4f}'.format(abs(s_xi2), abs(s_xi3), abs(s_xi4), abs(s_xi5), abs(s_fxi_xi2)))
        print('{:.2f} a0 + {:.2f} a1 + {:.2f} a2 + {:.2f} a3 = {:.4f}'.format(abs(s_xi3), abs(s_xi4), abs(s_xi5), abs(s_xi6), abs(s_fxi_xi3)))
        print('')
        print('a0 = '+str(abs(a_0)))
        print('a1 = '+str(abs(a_1)))
        print('a2 = '+str(abs(a_2)))
        print('a3 = '+str(abs(a_3)))
        print('')
        print('Polinomio de grado 3')
        print ('{:.4f} + {:.4f}x + {:.4f}x^2 + {:.4f}x^3'.format(abs(a_0), abs(a_1), abs(a_2), abs(a_3)))
        return polynomial_size, a_0, a_1
    
if __name__ == '__main__':
    minimum_squares ()