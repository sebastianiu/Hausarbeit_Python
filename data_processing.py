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
from sqlalchemy import create_engine,select,text,MetaData
from sqlalchemy.orm import declarative_base
from os import path
import sys

def data_import(file,table,databasename):     
    
    ''' Funktion zum Auslesen von Daten aus einer CSV-Datei und import in eine SQLLite-DB-Tabelle '''
    ''' Prüfen, ob datei im verzeichnis exitiert'''
    if path.exists(file):    
        '''Mit SQLite-Datenbank verbinden'''
        engine = create_engine(f'sqlite:///{databasename}.db',future = True,echo = True)   
         
        ''' Daten aus CSV-Dateu auslesen und in dataframe speichern '''
        data = pd.read_csv(file,header=0)    
    
        ''' Prüfen, ob Daten nicht schon vorhanden sind'''
        con = engine.connect()    
        result = con.execute(text(f'select * from {table}'))
               
        if len(result.all()) == 0:
            data.to_sql(table,con=engine,if_exists='append',index = False,index_label = 'recordid')  
            print(f'(data_import) Daten in Tabelle {table} importiert.\n')
        else:
           raise LookupError(f'(data_import) Es sind bereits Daten in der Tabelle "{table}" vorhanden. Daher werden keine neuen Daten importiert.')
          
    else:
        raise FileNotFoundError(f'(data_import) Datei "{file}" nicht im Verzeichnis gefunden.')



def tabellennamen(database):#columnname_1,columnname_2):
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect()   


'''Funktion liest Spalten aus einer Datenbanktabelle aus'''
def read_data(database,table,*columnames):#columnname_1,columnname_2):
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect() 
    
    ''' Prüfen, ob Tabelle vorhanden'''
   # metadata_obj = MetaData()
   # table_list = list()
   # for t in metadata_obj.sorted_tables:
   #     table_list.append(t.name)
   # if table not in table_list:        
    #    raise KeyError(f'Tabelle "{table}" existiert nicht in der Datenbank "{database}".')      
   # else:
    result = con.execute(text(f'select * from {table}'))
        
    ''' Prüfen, ob auslesbare Daten vorhanden'''             
    if len(result.all()) == 0:
         raise LookupError(f'Tabelle {table} enthält keine Daten')
    else:
        data = pd.read_sql_table(table, con, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=(columnames), chunksize=None)#(columnname_1,columnname_2), chunksize=None)
       #output_data = list()
            
        #for columname in columnames:
         #    columname = data[columname].values
          #   output_data.append(columname)
                    
        return data#output_data     

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

''' Daten für lineare Regression auslesen '''
#data_y1 = read_data(database,table,'x','y1')
#data_y2 = read_data(database,table,'x','y2')
#data_y3 = read_data(database,table,'x','y3')
#data_y4 = read_data(database,table,'x','y4')

''' lineare Regression berechnen'''
#lregr_y1= linear_regression_lsquare(data_y1[0],data_y1[1])
#lregr_y2= linear_regression_lsquare(data_y2[0],data_y2[1])
#lregr_y3= linear_regression_lsquare(data_y3[0],data_y3[1])
#lregr_y4= linear_regression_lsquare(data_y4[0],data_y4[1])

#data_visualization(data_y1[0],data_y1[1],lregr_y1[0],lregr_y1[1],'y1')
#data_visualization(data_y2[0],data_y2[1],lregr_y2[0],lregr_y2[1],'y2')
#data_visualization(data_y3[0],data_y3[1],lregr_y3[0],lregr_y3[1],'y3')
#data_visualization(data_y4[0],data_y4[1],lregr_y4[0],lregr_y4[1],'y4')
