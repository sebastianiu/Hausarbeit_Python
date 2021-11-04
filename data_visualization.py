'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

import matplotlib.pyplot as plt
import bokeh as bk
import numpy as np
import fnmatch
from user_exceptions import DataFrameEmptyError

def create_scatter_plot_fuer_daten_und_ideale_funktionen(daten,
                                                         liste_ideale_funktionen,
                                                         daten_ideale_funktionen,
                                                         titel):   
    ''' 
    Funktion erstellt ein Scatter-Plot reale Daten und passende ideale 
    Funktions-Daten
    '''     
    try:
        # Prüfen, ob Funktionsargumente Daten enthalten
        if len(liste_ideale_funktionen) > 0 and daten_ideale_funktionen.empty\
        == False and daten.empty == False:
           
            # Style festlegen 
            plt.style.use('ggplot') 
            
            # figure erzeugen 
            fig, ax = plt.subplots(figsize=(6,6)) 
        
            # Grid hinzufügen 
            ax.grid(True,color="k")           
           
            # Liste mit Farben 
            farben_liste1 = ['red','orange','yellow','green']
            
            farbenwahl_index = 0
            
            # Liste aller Y-Spalten erzeugen
            y_spalten = fnmatch.filter(daten.columns,'y*')
            
            # Alle Punkte der idealen Funktionen mit Zufallsfarben zeichnen
            for y_spalte in y_spalten:    
                     
                # x-/y-Werte aus Datenbanktabelle auslesen
                X = daten['x']
                Y = daten[y_spalte]    
                  
                # Zeichne Punkte
                ax.scatter(
                       X
                       ,Y
                       ,s = 75
                       ,c=farben_liste1[farbenwahl_index]
                       ,label = f'{y_spalte} (trainingsdaten)'
                       ) 
                
                farbenwahl_index += 1 
               
            farbenwahl_index = 0
            
            # Alle Punkte der idealen Funktionen zeichnen
            farben_liste_ideale_funktionen = ['blue','purple','midnightblue',
                                              'magenta']
            
            farbenwahl_index = 0
            
            # Alle Punkte der idealen Funktionen mit Zufallsfarben zeichnen
            for nr_ideale_funktion in liste_ideale_funktionen:    
                     
                # x-/y-Werte aus Datenbanktabelle auslesen
                X = daten_ideale_funktionen['x']
                Y = daten_ideale_funktionen[nr_ideale_funktion]    
                  
                # Zeichne Punkte
                ax.scatter(
                       X
                       ,Y
                       ,s = 5
                       ,c=farben_liste_ideale_funktionen[farbenwahl_index]
                       ,label = f'{nr_ideale_funktion} (ideale Funktion)'
                       ) 
                
                farbenwahl_index += 1  
                
            # Visualisierung mit definierten Parametern einblenden    
            plt.title(titel)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.show()
            
        else:
            raise DataFrameEmptyError
    # Fehlermeldung zeigen, wenn keine Daten zur Visualisierung übergeben werden       
    except DataFrameEmptyError:
        print(DataFrameEmptyError().error_message)