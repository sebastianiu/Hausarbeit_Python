"""
Hauptprogramm-Modul

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

## Module importieren
import data as db
import data_visualization as dv
import sys

## Benutzer-Abfrage zu Verzeichnis, aus dem CSV-Dateien geladen werden sollen
file_directory = input(
                 'PROGRAMM ZUR HAUSARBEIT des Kurses Programmieren ' 
                 'mit Python (DLMDWPMP01)\n'
                 '***********************************************************'
                 '**********\n'
                 'Bitte geben Sie das Verzeichnis an, aus dem die Datensätze '
                 'im CSV-Format geladen werden sollen\n (test.csv, train.csv, '
                 'ideal.csv).\n Programm kann mit "exit" beendet werden. '               
                 )

# Wenn User "exit" eingibt, dann Programm beenden
if file_directory == 'exit':
    sys.exit()
else:    
    pass  
     
## 1) Datenbank generieren
database_operativ = db.database()

# Klasse für Datenverarbeitungsprozesse erzeugen
dp = db.data_processing()

## 2) Daten aus CSV auslesen 
Daten_ideale_funktionen = dp.read_csv(f'{file_directory}ideal.csv')
Trainingsdaten = dp.read_csv(f'{file_directory}train.csv')
Testdaten = dp.read_csv(f'{file_directory}test.csv') 

## 3) Daten in Tabellen importieren 
dp.import_data(Daten_ideale_funktionen,'Ideale_Funktionen')
dp.import_data(Trainingsdaten,'Trainingsdaten')

# Trainingsdaten aus Datenbanktabelle auslesen
Trainingsdaten = dp.read_data('Trainingsdaten','x','y1','y2','y3','y4')  
                                         
# Daten der idealen Funktionen aus Datenbanktabelle auslesen
Daten_ideale_funktionen  = dp.read_data('Ideale_Funktionen','x',
                                        *[f'y{i}' for i in range(1,51)])

## 4) Beste Passungen ermitteln 
Daten_ideale_passungen = dp.get_fits_with_least_square_method(Trainingsdaten,
                                                    Daten_ideale_funktionen)

## 5) Passungen mit Testdaten validieren & Ergebnisse speichern
Testdaten_validiert = dp.validate_testdata(Daten_ideale_passungen,Testdaten,
                                            Daten_ideale_funktionen) 
# validierte Testdaten importieren
dp.import_data(Testdaten_validiert,'Testdaten')
   
#Liste der ermittelten idealen Funktionen erzeugen
Liste_ideale_funktion = list(Daten_ideale_passungen['ideal_funktion'])

# Daten der ermittelten idealen Funktionen auslesen
Daten_ermittelte_ideale_funktionen  = dp.read_data('Ideale_Funktionen','x',*Liste_ideale_funktion)  

## 6) Daten visualisieren
# Trainingsdaten mit ermittelten Ideal-Funktionen visualisieren
dv.create_scatter_plot(Trainingsdaten,Liste_ideale_funktion,
                                    Daten_ermittelte_ideale_funktionen,
                                    titel='Trainingsdaten & passende ideale '
                                    'Funktionen'
                                  )

# Testdaten mit ermittelten Ideal-Funktionen visualisieren
dv.create_scatter_plot(Testdaten,Liste_ideale_funktion,Daten_ermittelte_ideale_funktionen,
                                    titel='Testdaten & ermittelte Ideal-Funktionen'
                                  )  

# Testdaten mit validierten Ideal-Funktionen visualisieren
#dv.create_scatter_plot(Testdaten,ideale_Funktionen_validiert,Daten_ermittelte_ideale_funktionen,
dv.create_scatter_plot(Testdaten_validiert,Liste_ideale_funktion,Daten_ermittelte_ideale_funktionen,
                                    titel='validierte Testdaten & Ideal-Funktionen')  