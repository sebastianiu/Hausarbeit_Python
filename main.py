"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""
from file_import_export import import_csv_data,read_csv
from database import create_database_model 
from data_processing import read_data,data_import,get_fits_with_least_square_method
import pandas as pd


'''gewünschter Namen der SQLite-Datenbank definieren'''    
database='db_hausarbeit_1113'     #input('Definieren Sie einen Namen Für die Datenbank, die erzeugt werden muss (Programm mit "-exit" Beenden)')#'db_hausarbeit_13'  

try:      
    '''SQLite-Datenbank erzeugen'''
    create_database_model(database)
    
    '''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
    import_csv_data('ideal.csv','ideale_funktionen',database)
    import_csv_data('train.csv','trainingsdaten',database)

except:
    print('Fehler ist aufgetreten')

finally:                                     
    ''' 
    Beste passungen zwischen Trainingsdaten und ideal Funktionen ermitteln 
    '''
    Tabelle_Ideale_Funktionen = get_fits_with_least_square_method(database)
    
    #print(Tabelle_Ideale_Funktionen)
   
    print('-----Tabelle_Ideale_Funktionen------')
    print(Tabelle_Ideale_Funktionen)
    print('-'*15)
    print('\n')
    #print('-----Tabelle_max_Abw------')
    #print(Tabelle_max_Abw)
    #print('-'*15)
   
          
                                                                                        
 






         















