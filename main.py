"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""
from file_import_export import import_data,read_csv
from database import create_database_model 
from data_processing import read_data,get_fits_with_least_square_method
import pandas as pd
import numpy as np


'''gewünschter Namen der SQLite-Datenbank definieren'''    
database='db_hausarbeit_3'     #input('Definieren Sie einen Namen Für die Datenbank, die erzeugt werden muss (Programm mit "-exit" Beenden)')#'db_hausarbeit_13'  

try:      
    '''SQLite-Datenbank erzeugen'''
    create_database_model(database)
    
    '''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
    import_data(read_csv('ideal.csv'),'ideale_funktionen',database)
    import_data(read_csv('train.csv'),'trainingsdaten',database)

except:
    print('Fehler ist aufgetreten')

finally:                                     
    ''' 
    Beste Passungen zwischen Trainingsdaten und ideal Funktionen ermitteln 
    '''
    Tabelle_Ideale_Funktionen = get_fits_with_least_square_method(database)
    
   
    ''' Testdaten einlesen'''
    testdaten = read_csv('test.csv')
        
    
    ''' Leerer DF für Ergebnisse erzeugen '''
    ergebnisdaten = pd.DataFrame(columns=['x','y','delta_y','funkt_nr'])                           
                            
    ''' Abweichungen aller x,y-Paare aus Testdaten zu y-Werten der idealen 
    Funktion ermitteln
    '''
    for i in range(0,4):        
        
        ''' Differenzen der Testwerte zu den idealen funktion ermitteln'''
        funktion_ideal = Tabelle_Ideale_Funktionen.loc[i].at['ideal_funktion']
        
        daten_ideale_funktion = read_data(database,'ideale_funktionen','x',funktion_ideal) 

        ''' Tabellen über x mergen'''        
        join_table = pd.merge(testdaten, daten_ideale_funktion, on=["x"],how="inner")                   
        
        ''' Abweichungen ermitteln, negative Vorzeichen raus rechnen'''
        join_table['delta_y'] = abs(join_table['y']-  join_table[funktion_ideal])
        join_table['funkt_nr']= funktion_ideal       
               
        ''' Ergebnis speichern '''
        ergebnisdaten = pd.concat([ergebnisdaten,join_table[['x','y','delta_y','funkt_nr']]])
     
        
    
    ''' Daten auf geringste Abweichunng reduzieren '''    
    ergebnisdaten = pd.merge(
                            ergebnisdaten[['x','y','delta_y',]].groupby(['x','y']).min('delta_y'),
                             ergebnisdaten[['x','y','delta_y','funkt_nr']],
                             on=['x','y','delta_y'],how='left'
                             )    
    ''' Mximale Abweichung Trainingsdaten zu idealer Funktion dazu joinen '''
    ergebnisdaten = pd.merge(ergebnisdaten,
                             Tabelle_Ideale_Funktionen[['ideal_funktion','Max_Abweichung']]
                             ,left_on=['funkt_nr'],right_on=['ideal_funktion'],how='left')
    
    
    ergebnisdaten = ergebnisdaten.drop(columns='ideal_funktion')
    
    ''' 
    Fälle ausfiltern, in denen max. Abw. zwischen Trainingsd. und idealen Funktionen
    größer als max. Abweichung wischen Testdaten und idealen Funktionen
    '''   
    ergebnisdaten =  ergebnisdaten.where(
                                            (
                                                ergebnisdaten['Max_Abweichung'] /
                                                ergebnisdaten['delta_y']                                             
                                                ) <= np.sqrt(2)
                                            )
     
    '''Ermittle Inices leerer Zeilen '''
    droplist_index = ergebnisdaten.where(ergebnisdaten['x'] == None).index.tolist()
    
    '''Lösche leere Zeilen'''
    ergebnisdaten.drop(droplist_index,axis ='index')
    
    print(ergebnisdaten)    
    
    ergebnisdaten.to_csv('ergebnis.csv')
    
    
        
 
          
   # join_table.to_csv('join.csv')
          
          
          #join_table = pd.merge(join_table,{'ideal_funktion':funktion_ideal})
          
          
         #ergebnisdaten = ergebnisdaten.append(join_table)
           
      
   
    
   
    #print('-----Tabelle_Ideale_Funktionen------')
    #print(Tabelle_Ideale_Funktionen)
    #print('-'*15)
    #print('\n')
   
          
                                                                                        
 






         















