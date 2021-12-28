'''
Programmmodul für Funktionen zur Datenvisualisierung

zue Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

import matplotlib.pyplot as plt
import bokeh as bk
import numpy as np
import fnmatch
import user_exceptions as ue
import time as t
import pandas as pd

def create_scatter_plot(daten,liste_ideale_funktionen,daten_ideale_funktionen,titel): 
    ''' Funktion erstellt ein Scatter-Plot reale Daten und passende ideale 
    Funktions-Daten   '''     
    try:
        # Prüfen, ob Funktionsargumente Daten enthalten
        if type(liste_ideale_funktionen) == list and len(liste_ideale_funktionen) > 0:
            try:
                if type(daten_ideale_funktionen) == pd.DataFrame \
                    and daten_ideale_funktionen.empty == False\
                    and type(daten) == pd.DataFrame and daten.empty == False:
           
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
                               ,label = f'{y_spalte} (Daten)'
                               ) 
                        
                        farbenwahl_index += 1 
                       
                    farbenwahl_index = 0
                    
                    # Alle Punkte der idealen Funktionen zeichnen
                    farben_liste_ideale_funktionen = ['blue','purple','midnightblue',
                                                      'magenta']                   
                    
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
                    raise ue.DataFrameEmptyError
            # Fehlermeldung zeigen, wenn keine Daten zur Visualisierung übergeben werden       
            except ue.DataFrameEmptyError:
                print(f'(create_scatter_plot "{titel}") {ue.DataFrameEmptyError().error_message}')
        else:
            raise ue.ListEmptyError
    # Fehlermeldung zeigen, wenn keine Daten zur Visualisierung übergeben werden       
    except ue.ListEmptyError:
        print(f'(create_scatter_plot "{titel}") {ue.ListEmptyError().error_message}')
            