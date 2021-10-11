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


'''Funktion die eine ideale Trendlinie für x-/y-Werte mit least square ermittelt'''
def linear_regression_with_least_square(database,table,columnname_x,columnname_y):  
    
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect()    
    data = pd.read_sql_table(table, con, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=(columnname_x,columnname_y), chunksize=None)
    col_x = data[columnname_x].values   #con.execute(text(f'select {x} from {table}'))
    col_y = data[columnname_y].values   #con.execute(text(f'select {y} from {table}'))
    
    ''' Steigung der Geraden ermitteln'''    
    mean_x = np.mean(col_x)
    mean_y = np.mean(col_y)
     
    ''' Gesamtzahl der Werte''' 
    n = len(col_x)
    
    ''' Using the formula to calculate 'm' and 'c' '''
    numer = 0
    denom = 0
    for i in range(n):
        numer += (col_x[i] - mean_x) * (col_y[i] - mean_y)
        denom += (col_x[i] - mean_x) ** 2
        
    m = numer / denom
    c = mean_y - (m * mean_x)    
       
    ''' Plotting Values and Regression Line '''    
    max_x = np.max(col_x) + 100
    min_x = np.min(col_x) - 100
    
    ''' Calculating line values x and y '''
    x = np.linspace(min_x, max_x, 1000)
    y = c + m * x
     
    ''' Ploting Line '''
    plt.plot(x, y, color='#58b970', label='Regression Line')
    # Ploting Scatter Points
    plt.scatter(col_x, col_y, c='#ef5423', label=f'Scatter Plot {columnname_y}')
     
    # Titel hinzufügen
    plt.title(table)
    plt.xlabel(columnname_x)
    plt.ylabel(columnname_y)
    plt.legend()
    plt.show()   
    

def finding_fits(table1,table2):
    '''
    Funktion zur Ermittlung der vier besten Passungen aus Trainingsdaten 
    und idealen Funktionen durch Minimierung der quadratischen Abweichungen
    '''
    pass