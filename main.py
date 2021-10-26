"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""


''' Passende Funktionen aus Modulen importieren '''
from data_import_export import import_data,read_csv
from database import create_database_model 
from data_processing import read_data,get_fits_with_least_square_method,validate_testdata,read_data
from data_visualization import create_scatter_plot1,create_scatter_plot2


import matplotlib.pyplot as plt
import numpy as np
import random


'''gewünschter Namen der SQLite-Datenbank definieren'''    
database='db_hausarbeit_9'    
#input('Definieren Sie einen Namen Für die Datenbank, die erzeugt werden muss (Programm mit "-exit" Beenden)')#'db_hausarbeit_13'  

try:      
    '''SQLite-Datenbank erzeugen'''
    create_database_model(database)
    
    '''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
    import_data(read_csv('ideal.csv'),'ideale_funktionen',database)
    import_data(read_csv('train.csv'),'trainingsdaten',database)
    
    ''' 
    Beste Passungen zwischen Trainingsdaten und ideal Funktionen ermitteln 
    '''
    daten_ideale_passungen = get_fits_with_least_square_method(database) 

    ''' Testdaten einlesen''' 
    testdaten = read_csv('test.csv')   
       
    ''' Testdaten mit Kriterium in U-Abschnitt 2 validieren    '''
    testdaten_validiert = validate_testdata(daten_ideale_passungen,testdaten,database)  
  
    import_data(testdaten_validiert,'testdaten',database) 

except:
    print('Fehler ist aufgetreten')

finally:    
    
    ''' Testdaten zeichnen '''
    X = read_data(database,'testdaten','x')
    Y = read_data(database,'testdaten','y')                
   
    ''' Zeichne Punkte-Wolke '''
    plt.scatter(
           X
           ,Y
           ,c=["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
           ,label = 'testdaten'
           )   
   
    plt.title('titel')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()    
    
    ''' ideale Funktion zeichnen '''    
    liste_ideale_funktionen = set(read_data(database,'testdaten','funkt nr'))
    
    for funkt_nr in liste_ideale_funktionen:   
        X = read_data(database,'ideale_funktionen','x')
        Y = read_data(database,'ideale_funktionen',funkt_nr)                
   
        ''' Zeichne Punkte-Wolke '''
        plt.scatter(
               X
               ,Y
               ,c=["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
               ,label = 'funkt_nr'
               )   
       
    plt.title('Ergebnis')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()
               
                  
 






         















