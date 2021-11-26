"""
Hauptprogramm-Modul

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

# Passende Funktionen aus Modulen importieren
import database as db
import data_processing as dp    
import data_visualization as dv

# gewünschter Namen der SQLite-Datenbank definieren    
# database='db_hausarbeit_15'   

database = input(
                 'Definieren Sie einen Namen Für die Datenbank, die erzeugt '                 
                 'werden muss (Programm mit "exit" Beenden). Die CSV-Dateien '
                 'mit den Beispieldaten müssen im Programmverzeichnis liegen. '
                 )

if database == 'exit':
    exit()
else:
    pass    

 
# SQLite-Datenbank erzeugen
db.create_database_model(database)
    
# Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in \
# Tabellen importieren  
dp.import_data(dp.read_csv('ideal.csv'),'ideale_funktionen',database)
dp.import_data(dp.read_csv('train.csv'),'trainingsdaten',database)
    
# Trainingsdaten auslesen
trainingsdaten = dp.read_data(database,'trainingsdaten','x','y1','y2','y3','y4')    
                                                      
# Daten der idealen Funktionen auslesen
daten_ideale_funktionen  = dp.read_data(database,'ideale_funktionen','x',
                                         *[f'y{i}' for i in range(1,51)])
    
# Beste Passungen zwischen Trainingsdaten und ideal Funktionen ermitteln 
daten_ideale_passungen = dp.get_fits_with_least_square_method(trainingsdaten,daten_ideale_funktionen) 

# Testdaten einlesen 
testdaten = dp.read_csv('test.csv')   
       
# Testdaten mit Kriterium in U-Abschnitt 2 validieren    
testdaten_validiert = dp.validate_testdata(daten_ideale_passungen,testdaten,
                                            daten_ideale_funktionen)  
  
dp.import_data(testdaten_validiert,'testdaten',database) 
    
# Trainingsdaten auslesen
trainingsdaten = dp.read_data(database,'trainingsdaten','x','y1','y2','y3','y4')
    
# Validierte Testdaten auslesen
testdaten_validiert = dp.read_data(database,'testdaten','x','y')
    
# Liste aller ermittelten idealen Funktionen erzeugen    
liste_ermittelte_ideale_funktionen = set(list(dp.read_data(database,'testdaten',
                                                 'funkt_nr')['funkt_nr']))
# Daten der idealen Funktionen auslesen
daten_ideale_funktionen  = dp.read_data(database,'ideale_funktionen','x',
                                         *liste_ermittelte_ideale_funktionen)  
    
# Trainingsdaten visualisieren
dv.create_scatter_plot_fuer_daten_und_ideale_funktionen(
                                    trainingsdaten,
                                    liste_ermittelte_ideale_funktionen,
                                    daten_ideale_funktionen,
                                    titel='Trainingsdaten & passende ideale '
                                    'Funktionen'
                                  )
    
# Testdaten visualisieren
dv.create_scatter_plot_fuer_daten_und_ideale_funktionen(testdaten_validiert,
                                  liste_ermittelte_ideale_funktionen,
                                    daten_ideale_funktionen,
                                    titel='Validierte Testdaten'
                                  )  
   
    

    
    
               
                  
 






         















