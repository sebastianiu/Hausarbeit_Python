"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

''' Passende Funktionen aus Modulen importieren '''
from data_import_export import import_data,read_csv
from database import create_database_model 
from data_processing import read_data,get_fits_with_least_square_method,validate_testdata,read_data
from data_visualization import create_scatter_plot_fuer_daten_und_ideale_funktionen


'''gewünschter Namen der SQLite-Datenbank definieren'''    
database='db_hausarbeit_10'    
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
    print('Fehler sind aufgetreten')

finally:   
    ''' Trainingsdaten auslesen '''
    trainingsdaten = read_data(database,'trainingsdaten','x','y1','y2','y3','y4')
    
    ''' validierte Testdaten auslesen '''
    testdaten_validiert = read_data(database,'testdaten','x','y')
    
    ''' Lister aller ermittelten idealen Funktion erzeugen '''    
    liste_ideale_funktionen = set(list(read_data(database,'testdaten','funkt_nr')['funkt_nr']))
    
    '''Daten der idealen Funktionen auslesen'''
    daten_ideale_funktionen  = read_data(database,'ideale_funktionen','x',*liste_ideale_funktionen)
    
    '''Trainingsdaten visualisieren '''
    create_scatter_plot(
                                    trainingsdaten,
                                    liste_ideale_funktionen,
                                    daten_ideale_funktionen
                                  )
    
    ''' Testdaten visualisieren '''
    create_scatter_plot(testdaten_validiert,
                                  liste_ideale_funktionen,
                                    daten_ideale_funktionen
                                  )
    
    
    
               
                  
 






         















