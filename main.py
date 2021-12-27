"""
Hauptprogramm-Modul

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

# Passende Funktionen aus Modulen importieren
import data as db
import data_visualization as dv

#Benutzer-Abfrage zu Verzeichnis, wo Datenfiels leigen
file_directory = "E:/"
'''
input(
                 'PROGRAMM ZUR HAUSARBEIT des Kurses Programmieren ' 
                 'mit Python (DLMDWPMP01)\n'
                 '***********************************************************'
                 '**********\n'
                 'Bitte geben Sie das Verzeichnis an, aus dem die Datensätze '
                 'im CSV-Format geladen werden sollen (test.csv, train.csv, '
                 'ideal.csv). Programm kann mit "exit" beendet werden. '               
                 )
'''

if file_directory == 'exit':
    exit()
else:    
    pass   
     
## SQLite-Datenbank erzeugen
database_operativ = db.database()

#Klasse für Datenverarbeitungsprozesse erzeugen
dp = db.data_processing()

## Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen 
Daten_ideale_funktionen = dp.read_csv(f'{file_directory}ideal.csv')
Trainingsdaten = dp.read_csv(f'{file_directory}train.csv')
Testdaten = dp.read_csv(f'{file_directory}test.csv') 

## Daten in Tabellen importieren 
dp.import_data(Daten_ideale_funktionen,'Ideale_Funktionen')
dp.import_data(Trainingsdaten,'Trainingsdaten')

# Trainingsdaten auslesen
Trainingsdaten = dp.read_data('Trainingsdaten','x','y1','y2','y3','y4')  
                                         
# Daten der idealen Funktionen auslesen
Daten_ideale_funktionen  = dp.read_data('Ideale_Funktionen','x',
                                        *[f'y{i}' for i in range(1,51)])

## Beste Passungen zwischen Trainingsdaten und ideal Funktionen ermitteln 
Daten_ideale_passungen = dp.get_fits_with_least_square_method(Trainingsdaten,
                                                    Daten_ideale_funktionen)

# Testdaten mit Kriterium in U-Abschnitt 2 validieren    
ideale_Funktionen_validiert = dp.validate_testdata(Daten_ideale_passungen,Testdaten,
                                            Daten_ideale_funktionen) 
   
# Daten der ermittelten idealen Funktionen auslesen
Daten_ermittelte_ideale_funktionen  = dp.read_data('Ideale_Funktionen','x',*list(Daten_ideale_passungen['ideal_funktion']))  

# Trainingsdaten visualisieren
dv.create_scatter_plot_fuer_daten_und_ideale_funktionen(Trainingsdaten,
                                    list(Daten_ideale_passungen['ideal_funktion']),
                                    Daten_ermittelte_ideale_funktionen,
                                    titel='Trainingsdaten & passende ideale '
                                    'Funktionen'
                                  )

# Testdaten visualisieren
dv.create_scatter_plot_fuer_daten_und_ideale_funktionen(Testdaten,
                                  list(Daten_ideale_passungen['ideal_funktion']),
                                    Daten_ermittelte_ideale_funktionen,
                                    titel='Testdaten & ermittelte Ideal-Funktionen'
                                  )  




   
    

    
    
               
                  
 






         















