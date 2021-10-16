# -*- coding: utf-8 -*-
'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

'''erfoderliche Pakete importieren'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine,select,text

'''Funktion liest 2 Spalten aus einer Datenbanktabelle aus'''
def read_data(database,table,*columnames):#columnname_1,columnname_2):
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect()    
    data = pd.read_sql_table(table, con, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=(columnames), chunksize=None)#(columnname_1,columnname_2), chunksize=None)
    
    output_data = list()
    
    for columname in columnames:
        columname = data[columname].values
        output_data.append(columname)
        
    return output_data

''' Funktion ermittelt Formel für Regressionsgerade mit least-Square-Methodik'''
def linear_regression_lsquare(X,Y):      
    
    ''' Ermittle a und b für Trendgeraden-Formel y= a+b* x '''    
    ''' arithmn mitte für x und y berechnen'''    
    mean_x = np.mean(X)
    mean_y = np.mean(Y)
     
    ''' Gesamtzahl der x-Werte''' 
    n = len(X)
    
    ''' Werte zur Berechnung von b ermitteln'''
    Zaehler = 0
    Nenner = 0
    
    ''' Berechnung über alle Datenzeilen'''
    for i in range(n):
        Zaehler += (X[i] - mean_x) * (Y[i] - mean_y)
        Nenner += (X[i] -  mean_x) ** 2
        
    ''' Berechne a und b'''
    b = Zaehler / Nenner
    a = mean_y - (b * mean_x)   
    
    return [a,b]


def data_visualization(X,Y,a,b,titel):    
    ''' Zeichne x-,y-Werte und Regressionsgerade'''    
    max_x = np.max(X) #+ 100
    min_x = np.min(X) #- 100
    
    ''' Berechne x und y-Werte sowie Achsenabschnitte'''
    x_values = np.linspace(min_x, max_x, 10)
    y_values = a + b * x_values
     
    ''' Zeichne Gerade '''
    plt.plot(x_values, y_values, color='#58b970', label='Regressionsgerade')
    ''' Zeichne Scatter Points '''
    plt.scatter(X, Y, c='#ef5423', label=f'Scatter Plot')
     
    plt.title(titel)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()   
    

def finding_fits(table1,table2):
    '''
    Funktion zur Ermittlung der vier besten Passungen aus Trainingsdaten 
    und idealen Funktionen durch Minimierung der quadratischen Abweichungen
    '''
    pass