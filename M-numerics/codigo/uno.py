import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from colorama import init, Fore, Back, Style
from PyQt5.QtWidgets import (QTableWidget,QTableWidgetItem, QAbstractItemView)
from m_numerics import Ui_MainWindow
from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
import math
from sympy import Symbol
from sympy import cos
from sympy import sin
def divided_differences():
    #Leer Xi del usuario
    #Los while validan que el usuario escriba un valor correcto
    while True:
        try:
            iteration_num = int(input('¿Cuantas iteraciones vas a calcular? '))
            if iteration_num > 0  :
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
            if question.upper() in ['SI','NO']:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Variables inicializadas
    work = False
    user_xi = 0
    result = 0
    #Crea el polinomio en formato legible
    polynomial = lagrange(Xi, fXi)
    print ('Polinomio')
    print (polynomial)
    print_tableDD (Xi, fXi)
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
        result = calculateDD(Xi, fXi, user_xi, work)
        print (Fore.WHITE +'El resultado de f(Xi) en el punto Xi = {:.2f} es de {:.4f}'.format(user_xi, result))
        print(Fore.WHITE + "ADIOS")
        graphDD (Xi, fXi, user_xi, result, iteration_num, work)
    else:
        #Sin resultado
        graphDD (Xi, fXi, user_xi, result, iteration_num, work)

    
    
def calculateDD (Xi, fXi, user_xi, work):
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

def print_tableDD (Xi, fXi):
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
    
def graphDD (Xi, fXi, user_xi, result, iteration_num, work):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    if work == True:
        x = ([[None]]*(iteration_num+1))
        y = ([[None]]*(iteration_num+1))
        for i in range (0, iteration_num):
            x[i] = [Xi[i]]
            y[i] = [fXi[i]]
        x[iteration_num] = [user_xi]
        y[iteration_num] = [result]
        ui.MplWidget.canvas.axes.axvline(user_xi, color='r')
        ui.MplWidget.canvas.axes.axhline(result, color='r',)
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
    
    ui.MplWidget.canvas.axes.plot(x, y, '-o', c='b')
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('f(Xi)')
    ui.MplWidget.canvas.axes.set_title('Diferencias Divididas')
    MainWindow.show()

    sys.exit(app.exec_())

def minimum_squares():
    #Leer Xi del usuario
    #Los while validan que el usuario escriba un valor correcto
    while True:
        try:
            iteration_num = int(input('¿Cuantas iteraciones vas a calcular? '))
            if iteration_num > 0:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    print('Introduce los valores de Xi')
    Xi=np.array([0.00]*iteration_num, dtype=np.complex_)
    for i in range (0, iteration_num):
        while True:
            try:
                Xi[i] = complex(input('Xi en la posición {}: '.format(i)))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Leer f(Xi) del usuario
    print('Introduce los valores de f(Xi)')
    fXi=np.array([0.00]*iteration_num, dtype=np.complex_)
    for i in range (0, iteration_num):
        while True:
            try:
                fXi[i]=complex(input('f(Xi) en la posición {}: '.format(i)))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    polynomial_grade, coef_0, coef_1 = calculateMS(Xi, fXi)
    graphMS (Xi, fXi, iteration_num, polynomial_grade, coef_0, coef_1)
    
def graphMS (Xi, fXi, iteration_num, polynomial_grade, coef_0, coef_1):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
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
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('f(Xi)')
    ui.MplWidget.canvas.axes.set_title('Minimos Cuadrados')
    if polynomial_grade == 1:
        ui.MplWidget.canvas.axes.scatter(Xi, fXi)
        x_g = np.array([min(Xi), max(Xi)])
        fun = coef_1 * x_g + coef_0
        ui.MplWidget.canvas.axes.plot(x_g, fun)
        ui.MplWidget.canvas.axes.show()
    else:
        ui.MplWidget.canvas.axes.plot(x, y, '-o', c='b') 
    MainWindow.show()

    sys.exit(app.exec_()) 

def calculateMS (Xi, fXi):
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
                    print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
                
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
        print(Fore.WHITE +'Polinomio de grado 1')
        print(Fore.WHITE +'{:.4f} + {:.4f}x'.format(abs(a_0), abs(a_1)))
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
        print(Fore.WHITE +'Polinomio de grado 2')
        print (Fore.WHITE +'{:.4f} + {:.4f}x + {:.4f}x^2'.format(abs(a_0), abs(a_1), abs(a_2)))
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
        print(Fore.WHITE +'Polinomio de grado 3')
        print (Fore.WHITE +'{:.4f} + {:.4f}x + {:.4f}x^2 + {:.4f}x^3'.format(abs(a_0), abs(a_1), abs(a_2), abs(a_3)))
        return polynomial_size, a_0, a_1

def lagrangeM ():
    #Leer Xi del usuario
    #Los while validan que el usuario escriba un valor correcto
    while True:
        try:
            iteration_num = int(input('¿Cuantas iteraciones vas a calcular? '))
            if iteration_num > 0:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    print('Introduce los valores de Xi')
    Xi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                Xi[i] = float(input('Xi en la posición {}: '.format(i)))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Leer f(Xi) del usuario
    print('Introduce los valores de f(Xi)')
    fXi=np.array([0.00]*iteration_num)
    for i in range (0, iteration_num):
        while True:
            try:
                fXi[i]=float(input('f(Xi) en la posición {}: '.format(i)))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Lee la posicion de X que busca el usuario
    while True:
        try:
            question = str(input('¿Deseas calcular algún valor? || Si/No '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #Variables inicializadas
    work = False
    user_xi = 0
    result = 0
    polynomial = lagrange(Xi, fXi)
    print (Fore.WHITE +'Polinomio')
    print (polynomial)
    print_tableL (Xi, fXi, iteration_num)
    if question.upper() == 'SI':
        while True:
            try:
                user_xi = float (input('¿Qué valor deseas calcular? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        #Con resultado
        work = True
        #Aqui va el resultado
        result = calculateL(Xi, fXi, user_xi)
        print (Fore.WHITE +'El resultado de f(Xi) en el punto Xi = {:.2f} es de {:.4f}'.format(user_xi, result))
        graphL (Xi, fXi, user_xi, result, iteration_num, work)
        
    else:
        #Sin resultado
        graphL(Xi, fXi, user_xi, result, iteration_num, work)
    #Crea el polinomio en formato legible
    

def calculateL (Xi, fXi, user_xi):      
    polynomial = lagrange(Xi, fXi)
    print (Fore.WHITE +'Polinomio')
    print (polynomial)
    lag_result = polynomial(user_xi)
    print (lag_result)
    return lag_result

def print_tableL (Xi, fXi, iteration_num):
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi', 'f(Xi)']
    for i in range (0, iteration_num):
        table[i] = [i, Xi[i], fXi[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid'))
    
def graphL(Xi, fXi, user_xi, result, iteration_num, work):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    if work == True:
        x = ([[None]]*(iteration_num+1))
        y = ([[None]]*(iteration_num+1))
        for i in range (0, iteration_num):
            x[i] = [Xi[i]]
            y[i] = [fXi[i]]
        x[iteration_num] = [user_xi]
        y[iteration_num] = [result]
        ui.MplWidget.canvas.axes.axvline(user_xi, color='r')
        ui.MplWidget.canvas.axes.axhline(result, color='r',)
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

    ui.MplWidget.canvas.axes.plot(x, y, '-o', c='b')
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('f(Xi)')
    ui.MplWidget.canvas.axes.set_title('Diferencias Divididas')
    MainWindow.show()

    sys.exit(app.exec_())

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
    print_tableFP(solve_xi, solve_xd, solve_xm, solve_f_xm)
    graphFP(solve_xi, solve_xd)
    
def print_tableFP(results_xi, results_xd, results_xm, results_f_xm):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'Xd', 'Xm', '|f(Xm)|']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_xd[i], results_xm[i], results_f_xm[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xm[n-1]))
    
def graphFP (results_xi, results_xd):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    iteration_num = len(results_xi)
    x = ([[None]]*(iteration_num))
    y = ([[None]]*(iteration_num))      
    for i in range (0, iteration_num):
        x[i] = [results_xi[i]]
        y[i] = [results_xd[i]]
    ui.MplWidget.canvas.axes.plot(x, y, '-o', c='b')
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('Xd')
    ui.MplWidget.canvas.axes.set_title('Posición Falsa')
    MainWindow.show()

    sys.exit(app.exec_())

def RK ():
    #
    #Lee x(0) y x(1)
    #
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                x = float(input('¿Cuanto vale x(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                x_final = float(input('¿Cuanto vale x(final)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee y(0)
    #
    while True:
            try:
                y = float(input('¿Cuanto vale y(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Pregunta si se conoce el valor de n o h
    #
    while True:
        try:
            question = str(input('¿Conoces n o h? Escribe n || h: '))
            if question.upper() in ['N', 'H']:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
                    print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Hace las iteraciones
    #
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
        k_0 = expr
        k_1 = (x + h) - (y + (h*k_0))
        y = y + (h/2*(k_0 + k_1))
        x = x + h
        solve_x.append(x)
        solve_y.append(y)
    print_tableRK(solve_x, solve_y)
    graphRK(solve_x, solve_y)

def graphRK (results_x, results_y):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
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
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('Yi')
    ui.MplWidget.canvas.axes.set_title('Runge - Kutta 2° orden')
    ui.MplWidget.canvas.axes.plot(x, y, c='b')
    MainWindow.show()

    sys.exit(app.exec_()) 
    
def print_tableRK (results_x, results_y):
    iteration_num = len(results_x)
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi 2o Orden', 'Yi 2o Orden']
    for i in range (0, iteration_num):
        table[i] = [i, results_x[i], results_y[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    res = results_y[iteration_num-1]
    print(Fore.WHITE +'Resultado de y(?) = '+str(res))

def bis ():
    #
    #Lee Xi y XD
    #
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                Xi = int(input('¿Cuanto vale Xi? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                Xd = int(input('¿Cuanto vale Xd? '))
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
    #Lee el error
    while True:
        try:
            print('Ejemplo de error: 1x10-³ --> 0.001')
            error = float(input('Escribe el tamaño del error: '))
            break
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
        print(Fore.WHITE +'El problema tiene solucion')
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
        print(Fore.WHITE +'El problema NO tiene solucion')
        sys.exit() #Corta el programa
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de solucion es = '+str(Xm))
    graphBis(solve_xi, solve_xd)
    

def graphBis (results_xi, results_xd):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    iteration_num = len(results_xi)
    iteration_num = iteration_num - 1
    if results_xi[0] < results_xi[iteration_num] and results_xd[0] < results_xd[iteration_num]:
        results_xi.sort()
        results_xd.sort()
    else:
        if results_xi[0] > results_xi[iteration_num] and results_xd[0] > results_xd[iteration_num]:
            results_xi.sort(reverse=True)
            results_xd.sort(reverse=True)
        else:
            if results_xi[0] > results_xi[iteration_num]:
                results_xi.sort(reverse=True)
                results_xd.sort()
            else:
                if results_xd[0] > results_xd[iteration_num]:
                    results_xi.sort()
                    results_xd.sort(reverse=True)

        ui.MplWidget.canvas.axes.set_xlabel("Xi")
        ui.MplWidget.canvas.axes.set_ylabel("Xd")
        ui.MplWidget.canvas.axes.set_title("Xi y Xd")
        ui.MplWidget.canvas.axes.plot(results_xi, results_xd,"-o", c="b")
        MainWindow.show()
        sys.exit(app.exec_()) 
    
def RKcuarto ():
#
#Lee x(0) y x(1)
#
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                x = float(input('¿Cuanto vale x(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                x_final = float(input('¿Cuanto vale x(final)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee y(0)
    #
    while True:
            try:
                y = float(input('¿Cuanto vale y(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Pregunta si se conoce el valor de n o h
    #
    while True:
        try:
            question = str(input('¿Conoces n o h? Escribe n || h: '))
            if question.upper() in ['N', 'H']:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
                    print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
        k_1 = function(expr, x, y)
        k_2 = function(expr, (x + 0.5*h), (y + 0.5*k_1*h))
        k_3 = function(expr, (x + 0.5*h), (y + 0.5*k_2*h))
        k_4 = function(expr, (x + h), (y + k_3*h))
        y = y + (1.0/6.0)*(k_1 + 2*k_2 + 2*k_3 + k_4)*h
        x = x + h
        solve_x.append(x)
        solve_y.append(y)
    print_tableRKC(solve_x, solve_y)
    graphRKC(solve_x, solve_y)

def function(expr, x, y):
    return expr

def graphRKC (results_x, results_y):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
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
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('Yi')
    ui.MplWidget.canvas.axes.set_title('Runge - Kutta 4° orden')
    ui.MplWidget.canvas.axes.plot(x, y, c='b')
    MainWindow.show()
    sys.exit(app.exec_())
    
def print_tableRKC (results_x, results_y):
    iteration_num = len(results_x)
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi 2o Orden', 'Yi 2o Orden']
    for i in range (0, iteration_num):
        table[i] = [i, results_x[i], results_y[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    res = results_y[iteration_num-1]
    print('Resultado de y(?) = '+str(res))
def newton():
    #
    #Lee Xo
    #
    while True:
        try:
            Xo = float(input('¿Cuanto vale Xo? '))
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
    #Hace las iteraciones
    x = Symbol('x')
    expr = eval(f)
    derived = expr.diff(x)
    print(Fore.WHITE +'La derivada de la función es : '+str(derived))
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
    print_tableNR(solve_xo, solve_error)
    
def print_tableNR(results_xo, results_error):
    n = len(results_xo)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xo', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xo[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xo[n-1]))

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
    print_tableSEC(solve_xi, solve_error)
    
def print_tableSEC(results_xi, results_error):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xi[n-1]))

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
    print_tableSP(solve_xi, solve_g_xi, solve_error)
def print_tableSP(results_xi, results_g_xi, results_error):
    n = len(results_xi)
    table = ([[None]]*n)
    headers = ['Iteraciones', 'Xi', 'g(Xi)', 'Error']
    for i in range (0, n):
        table[i] = [i, results_xi[i], results_g_xi[i], results_error[i]]
    
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".6f"))
    print(Fore.WHITE +'La raiz de convergencia es: '+str(results_xi[n-1]))

def euler ():
    #
    #Lee x(0) y x(1)
    #
    print('Ingresa los intervalos para calcular las iteraciones')
    while True:
            try:
                x = float(input('¿Cuanto vale x(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    while True:
            try:
                x_final = float(input('¿Cuanto vale x(final)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Lee y(0)
    #
    while True:
            try:
                y = float(input('¿Cuanto vale y(0)? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Pregunta si se conoce el valor de n o h
    #
    while True:
        try:
            question = str(input('¿Conoces n o h? Escribe n || h: '))
            if question.upper() in ['N', 'H']:
                break
            else:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
        except ValueError:
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Cuando la respuesta es n
    #
    if (question == 'n'):
        while True:
            try:
                n = int(input('¿Cuantos subintervalos va a calcular? '))
                break
            except ValueError:
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
                print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
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
            print(Fore.RED + "O P C I Ó N   N O   V A L I D A")
    #
    #Hace las iteraciones
    #
    solve_x = []
    solve_y = []
    solve_x.append(x)
    solve_y.append(y)
    for i in range (0, n):
        expr = eval(f)
                #Despues de la h va la funcion
        y = y + (h*(expr))
        x = x + h
        solve_x.append(x)
        solve_y.append(y)
    print_tableEul(solve_x, solve_y)
    graphEul(solve_x, solve_y)
    

def graphEul (results_x, results_y):
    app = QtWidgets.QApplication(sys.argv)                
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
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
    ui.MplWidget.canvas.axes.set_xlabel('Xi')
    ui.MplWidget.canvas.axes.set_ylabel('Yi')
    ui.MplWidget.canvas.axes.set_title('Euler')
    ui.MplWidget.canvas.axes.plot(x, y)
    MainWindow.show()
    sys.exit(app.exec_())
    
def print_tableEul (results_x, results_y):
    iteration_num = len(results_x)
    table = ([[None]]*iteration_num)
    headers = ['Iteraciones', 'Xi', 'Yi']
    for i in range (0, iteration_num):
        table[i] = [i, results_x[i], results_y[i]]
        
    print (tabulate(table, headers, tablefmt='fancy_grid', floatfmt = ".4f"))
    print (Fore.WHITE +'Resultado')
    print(Fore.WHITE +'y(final) = {}'.format(str(results_y[iteration_num-1])))
        
