'''
Programmmodul für Datenverarbeitungs-Funktionen 
fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit 
Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

# Erfoderliche Pakete importieren
from sqlalchemy import create_engine,select,text,MetaData
from sqlalchemy.orm import declarative_base
from os import path
import sys
import numpy as np
import pandas as pd
from user_exceptions import DatabaseFileNotFoundError,DatabaseTableEmptyError

def read_data(database,table,*columnames):
    '''Funktion liest Spalten aus einer Datenbanktabelle aus und speichert Inhalt \
    in einem DataRame
    '''
    try:
        # Prüfen, ob DB-Datei exisiert
        if path.exists(f'{database}.db'):            
            # Mit SQLite-Datenbank verbinden'''
            engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True)   
            
            # Prüfen, ob auslesbare Daten vorhanden
            try:               
                with engine.connect() as con:
                    # Daten aus Tabelle abfragen
                    result = con.execute(text(f'select * from {table}'))
                    
                    if len(result.all()) > 0:
                        data = pd.read_sql_table(
                                                table, con, schema=None, index_col=None, 
                                                 coerce_float=True, parse_dates=None, 
                                                 columns=(columnames), chunksize=None
                                                )                    
                        return data                
                    else:
                        raise DatabaseTableEmptyError                     
            except DatabaseTableEmptyError:
                print(DatabaseTableEmptyError().error_message) 
                
        else:
            raise DatabaseFileNotFoundError
            
    except DatabaseFileNotFoundError:
        print(DatabaseFileNotFoundError().error_message) 
    
def get_fits_with_least_square_method(trainingsdaten,daten_ideale_funktionen):
    
    ''' Funktion, um die vier besten Passungen zwischen Trainingsdaten und idealen 
    Funktionen mit least suqare Methode zu ermittelt und zusätzliche die maximale 
    Abweichung je idealer Funktion zu den Trainingsdaten speichert
    '''
    # Leerer Dataframe für Selektions-Ergebnisse
    Tabelle_Ideale_Funktionen_tmp = pd.DataFrame(columns=['train_funktion', 
                                                           'ideal_funktion', 
                                                            'quadr_abw']
                                                 )
    
    # quadr. Abweichungen zwischen Trainingsdaten und idealen Funktionen ermitteln
    for i in range(1,5): 
        funktion_train = f'y{i}'
        Selektion_tmp = list()
        
        for i in range(1,51):        
            funktion_ideal= f'y{i}'        
            
            # Daten auslesen            
            data_funktion_train = trainingsdaten.filter(items=['x', 
                                                               funktion_train])            
            data_funktion_ideal =daten_ideale_funktionen.filter(items=['x', 
                                                               funktion_ideal])          
                        
            # Tabellen joinen und Abweichung pro Datenzeile ermitteln und 
            # Gesamtsumme aus quadr. Abweichen bilden'''        
            if funktion_train == funktion_ideal:
                join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'),
                                                     on='x',rsuffix='_ideal')
                quadr_abw =  sum((join_table[funktion_train] - 
                                  join_table[f'{funktion_ideal}_ideal'])**2)
            else:
                join_table= data_funktion_train.join(
                                    data_funktion_ideal.set_index('x'),on='x'
                                    )
                quadr_abw =  sum((
                                    join_table[funktion_train] - 
                                    join_table[funktion_ideal]
                                  )**2)
            
            # Alle Abweichungen je Trainingsdatenfunktion speichern
            Selektion_tmp.append({'train_funktion':funktion_train,'ideal_funktion':
                                  funktion_ideal,'quadr_abw':quadr_abw})     
    
        # Ideale Funktionen mit mit minimalster Abweichung ermitteln
        Selektion_tmp = pd.DataFrame(Selektion_tmp)
        
        Tabelle_Ideale_Funktionen_tmp = Tabelle_Ideale_Funktionen_tmp.append(
                Selektion_tmp.loc[
                                Selektion_tmp['quadr_abw'] == 
                               min(Selektion_tmp['quadr_abw'])]
                ) 

    
    # Ermittle maximale Abweichung zwischen tainingsdaten zu Werten der vier 
    # idealen Funktionen
    Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 
                                                      'ideal_funktion', 
                                              'Max_Abweichung'])     
   
    # maximale Abweichung je idealer Funktion
    for i in range(1,5):
          funktion_train = f'y{i}'
          
          
          data_funktion_train = trainingsdaten.filter(items=['x', 
                                                             funktion_train])         
          
          
          funktion_ideal = Tabelle_Ideale_Funktionen_tmp.loc[
                                Tabelle_Ideale_Funktionen_tmp['train_funktion'] 
                                   == funktion_train].iloc[0]['ideal_funktion']
          
          data_funktion_ideal = daten_ideale_funktionen.filter(items=['x', 
                                                               funktion_ideal])
                   
          # Tabellen joinen und Abweichungen pro Datenzeile ermitteln'''        
          if funktion_train == funktion_ideal:             
              join_table = pd.merge(trainingsdaten, daten_ideale_funktionen, on="x", 
                                    how="left",rsuffix='_ideal')
                                                     
              # Abweichung pro Zeile ermitteln
              join_table['Abweichung'] = join_table[funktion_train] - \
                                          join_table[f'{funktion_ideal}_ideal']
               
          else:
              join_table= pd.merge(trainingsdaten, daten_ideale_funktionen, 
                                   on="x", how="left")
                       
              # Abweichung pro Zeile ermitten
              join_table['Abweichung'] = join_table[funktion_train] - \
                                          join_table[funktion_ideal]
         
          # Zeile mit höchster Abweichung selektieren und in Dataframe speichern
          Max_Abweichung =  join_table.loc[join_table['Abweichung'] == 
                               max(join_table['Abweichung'])].iloc[0]['Abweichung']
          
          Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                                              {
                                              'train_funktion':funktion_train,
                                              'ideal_funktion':funktion_ideal,
                                              'Max_Abweichung':Max_Abweichung
                                              },ignore_index=True)         
         
    return Tabelle_Ideale_Funktionen       
   
def validate_testdata(finale_ideale_funktionen,testdaten,daten_ideale_funktionen):   
    ''' 
    Funktion um Testdaten zu validieren, d. h. X-Y-Paare selektieren, die das Kriterium 
    in U-Abschnitt 2 erfüllen und in DataFrame ausgeben
    '''     
    
    # Leerer DataFrame für Ergebnisse erzeugen
    ergebnisdaten = pd.DataFrame(columns=['x','y','delta_y','funkt_nr'])                           
                            
    # Abweichungen aller x,y-Paare aus Testdaten zu y-Werten der idealen 
    # Funktion ermitteln
    for i in range(0,4):        
        
        # Werte der idealen funktion auslesen
        funktion_ideal = finale_ideale_funktionen.loc[i].at['ideal_funktion']
        
        # Trainingsdaten auslesen
        data_funktion_ideal =daten_ideale_funktionen.filter(items=['x', 
                                                               funktion_ideal])      

        # Tabellen über x mergen       
        join_table = pd.merge(testdaten, data_funktion_ideal, on=["x"],
                              how="inner")                   
        
        # Abweichungen ermitteln, negative Vorzeichen raus rechnen
        join_table['delta_y'] = abs(join_table['y'] - join_table[funktion_ideal])
        join_table['funkt_nr']= funktion_ideal       
               
        # Ergebnis speichern
        ergebnisdaten = pd.concat([ergebnisdaten,join_table[['x','y','delta_y',
                                                             'funkt_nr']]])        
    
    # Daten auf geringste Abweichung reduzieren   
    ergebnisdaten = pd.merge(
                            ergebnisdaten[['x','y','delta_y',]].groupby(['x','y']).min('delta_y'),
                             ergebnisdaten[['x','y','delta_y','funkt_nr']],
                             on=['x','y','delta_y'],how='left'
                             )    
    # Maximale Abweichung Trainingsdaten zu idealer Funktion dazu joinen 
    ergebnisdaten = pd.merge(ergebnisdaten,
                             finale_ideale_funktionen[['ideal_funktion','Max_Abweichung']]
                             ,left_on=['funkt_nr'],right_on=['ideal_funktion'],how='left')
    
    #überflüssige Spalte löschen
    ergebnisdaten = ergebnisdaten.drop(columns='ideal_funktion')    
    
    # Löschen Datenzeilen , in denen Abweichung um mehr als Faktor Wurzel 2 größer 
    # als max. Abweichung zwischen Trainingsdaten und idealer Funktion
    ergebnisdaten.drop(ergebnisdaten[                                                                            
                                        (          
                                        ergebnisdaten['delta_y'] / 
                                        ergebnisdaten['Max_Abweichung']
                                        )  > np.sqrt(2)
                                    ].index, inplace=True                                     
                                     )
    #überflüssige Spalte löschen
    ergebnisdaten = ergebnisdaten.drop(columns='Max_Abweichung')
    
    return ergebnisdaten
