'''
Programmmodul für Datenverarbeitungs-Funktionen 

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

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
import  user_exceptions as ue
import fnmatch


def read_csv(file): 
    ''' Funktion zum Auslesen von Daten aus einer CSV-Datei'''
    try:
        # Prüfen, ob Datei im verzeichnis exitiert
        if path.exists(file) == True:   
            # Prüfen, ob es sich um eine CSV-Datei handelt
            try:
                if file.endswith('csv') == True:
                    # Daten aus CSV-Datei auslesen und in dataframe speichern
                    data = pd.read_csv(file,header=0)        
                    return data
                else:                    
                    raise ue.WrongFileFormatError
            except ue.WrongFileFormatError:
                print(ue.DataFrameEmptyError().error_message)                
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f'(data_import) Datei "{file}" nicht im Verzeichnis gefunden.')
     
def import_data(data,table,databasename):    
    ''' Funktion zum Auslesen von Daten aus einer CSV-Datei und import in eine 
    SQLLite-DB-Tabelle 
    ''' 
    try:
        if data.empty == False:            
            try:
                # Prüfen, ob SQLite-Datenbank-Datei im Verzeichnis exitiert
                if path.exists(f'{databasename}.db') == True: 
                    
                    try:
                        # Mit SQLite-Datenbank verbinden
                        engine = create_engine(f'sqlite:///{databasename}.db',
                                               future = True,echo = True)
                       
                        # Prüfen, ob Daten nicht schon vorhanden sind
                        with engine.connect() as con:
                            # Daten aus Tabelle abfragen
                            result = con.execute(text(f'select * from {table}'))    
                           
                            if len(result.all()) == 0:                   
                                # Daten importieren
                                data.to_sql(table,con=engine,
                                            if_exists='append',
                                            index = False,
                                            index_label = 'recordid'
                                            )  
                                print(f'(data_import) Daten in Tabelle {table} '
                                      'importiert.\n')
                            else:
                               raise ue.DatabaseTableAlreadyFullError  
                    except ue.DatabaseTableAlreadyFullError:
                        print(ue.DatabaseTableAlreadyFullError().error_message)
                else:
                    raise ue.DatabaseFileNotFoundError
                    
            except ue.DatabaseFileNotFoundError:
                print(ue.DatabaseFileNotFoundError().error_message)
            else:
                raise ue.DataFrameEmptyError 
            
    except ue.DataFrameEmptyError:
        print(ue.DataFrameEmptyError().error_message)


def read_data(database,table,*columnames):
    '''Funktion liest Spalten aus einer Datenbanktabelle aus und speichert Inhalt \
    in einem DataRame
    '''
    try:
        # Prüfen, ob DB-Datei exisiert
        if path.exists(f'{database}.db'):            
            # Mit SQLite-Datenbank verbinden'''
            engine = create_engine(f'sqlite:///{database}.db',future = True,
                                   echo = True)   
            
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
                        raise ue.DatabaseTableEmptyError                     
            except ue.DatabaseTableEmptyError:
                print(ue.DatabaseTableEmptyError().error_message) 
                
        else:
            raise ue.DatabaseFileNotFoundError
            
    except ue.DatabaseFileNotFoundError:
        print(ue.DatabaseFileNotFoundError().error_message) 
    
def get_fits_with_least_square_method(trainingsdaten,daten_ideale_funktionen):    
    ''' Funktion, um die vier besten Passungen zwischen Trainingsdaten und 
    idealen Funktionen mit least suqare Methode zu ermittelt und 
    zusätzliche die maximale Abweichung je idealer Funktion zu den 
    Trainingsdaten speichert
    '''
    
    try:
        # Prüfen, ob Funktionsargumente Daten enthalten
        if trainingsdaten.empty == False \
           and daten_ideale_funktionen.empty == False:
            
            # Leerer Dataframe für Selektions-Ergebnisse erzeugen
            Tabelle_Ideale_Funktionen_tmp = pd.DataFrame(columns=['train_funktion', 
                                                               'ideal_funktion', 
                                                                'quadr_abw']
                                                     )    
        
            # quadr. Abweichungen zwischen Trainingsdaten und idealen 
            # Funktionen ermitteln 
            
            # Zwei Listen aller Y-Spalten in Traininsgdaten und idealen 
            # Funktionen erzeugen
            trainingsdaten_y_spalten = fnmatch.filter(trainingsdaten.columns,
                                                      'y*')            
            ideale_funktionen_y_spalten = fnmatch.filter(
                                        daten_ideale_funktionen.columns,'y*')
            
            for funktion_train in trainingsdaten_y_spalten:
                
                Selektion_tmp = list()
                
                for funktion_ideal in ideale_funktionen_y_spalten:
                    
                    # Daten auslesen            
                    data_funktion_train = trainingsdaten.filter(items=['x',
                                                            funktion_train])
                    
                    data_funktion_ideal =daten_ideale_funktionen.filter(
                                                                    items=['x', 
                                                                funktion_ideal]
                                                                 )          
                                
                    # Tabellen joinen und Abweichung pro Datenzeile ermitteln 
                    # und Gesamtsumme aus quadr. Abweichen bilden'''        
                    if funktion_train == funktion_ideal:
                        join_table= data_funktion_train.join(
                                                data_funktion_ideal.set_index('x'),
                                                on='x',
                                                rsuffix='_ideal'
                                             )
                        quadr_abw =  sum(
                                            (
                                            join_table[funktion_train] - 
                                             join_table[f'{funktion_ideal}_ideal']
                                             )**2)
                    else:
                        join_table= data_funktion_train.join(
                                            data_funktion_ideal.set_index('x'),
                                            on='x'
                                            )
                        quadr_abw =  sum((
                                            join_table[funktion_train] - 
                                            join_table[funktion_ideal]
                                          )**2)
                    
                    # Alle Abweichungen je Trainingsdatenfunktion speichern
                    Selektion_tmp.append({'train_funktion':funktion_train,
                                          'ideal_funktion': funktion_ideal,
                                          'quadr_abw':quadr_abw})     
            
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
           
            # maximale Abweichung je Trainingsdatenfunktion und idealer Funktion 
            # ermitteln
            for funktion_train in trainingsdaten_y_spalten:
                  data_funktion_train = trainingsdaten.filter(items=['x', 
                                                            funktion_train])                  
                  
                  funktion_ideal = Tabelle_Ideale_Funktionen_tmp.loc[
                                        Tabelle_Ideale_Funktionen_tmp['train_funktion'] 
                                           == funktion_train].iloc[0]['ideal_funktion']
                  
                  data_funktion_ideal = daten_ideale_funktionen.filter(
                                                               items=['x', 
                                                               funktion_ideal]
                                                                )
                           
                  # Tabellen joinen und Abweichungen pro Datenzeile ermitteln        
                  if funktion_train == funktion_ideal:             
                      join_table = pd.merge(data_funktion_train, 
                                            data_funktion_ideal, 
                                            on="x",how="left",rsuffix='_ideal')
                                                             
                      # Abweichung pro Zeile ermitteln
                      join_table['Abweichung'] = join_table[funktion_train] - \
                                                  join_table[f'{funktion_ideal}_ideal']
                       
                  else:
                      join_table= pd.merge(data_funktion_train, data_funktion_ideal, 
                                           on="x", how="left")
                               
                      # Abweichung pro Zeile ermitten
                      join_table['Abweichung'] = join_table[funktion_train] - \
                                                  join_table[funktion_ideal]
                 
                  # Zeile mit höchster Abweichung selektieren und in Dataframe 
                  # speichern
                  Max_Abweichung =  join_table.loc[join_table['Abweichung'] == 
                        max(join_table['Abweichung'])].iloc[0]['Abweichung']
                  
                  Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                                          {
                                            'train_funktion' : funktion_train,
                                            'ideal_funktion' : funktion_ideal,
                                            'Max_Abweichung' : Max_Abweichung
                                            },ignore_index=True)
            return Tabelle_Ideale_Funktionen 
        else:
            raise ue.DataFrameEmptyError
    except ue.DataFrameEmptyError:
            print(ue.DataFrameEmptyError().error_message) 
   
def validate_testdata(ideale_passungen,testdaten,gesamtdaten_ideale_funktionen):   
    ''' 
    Funktion um Testdaten zu validieren, d. h. X-Y-Paare selektieren, die das 
    Kriterium in U-Abschnitt 2 erfüllen und in DataFrame ausgeben
    '''    
    try:
        # Prüfen, ob alle Funktionsargumente Daten enthalten
        if ideale_passungen.empty == False \
        and testdaten.empty == False  \
        and gesamtdaten_ideale_funktionen.empty == False:
     
            # Leerer DataFrame für Ergebnisse erzeugen
            ergebnisdaten = pd.DataFrame(columns=['x','y','delta_y','funkt_nr'])                           
                                    
            # Abweichungen aller x,y-Paare aus Testdaten zu y-Werten der idealen 
            # Funktion ermitteln     
            
            for i in range(0,len(ideale_passungen)): 
            #for funktion_ideal in ideale_funktionen_y_spalten:
                
                # Werte der idealen funktion auslesen
                funktion_ideal = ideale_passungen.loc[i].at['ideal_funktion']
                
                # Trainingsdaten auslesen
                data_funktion_ideal = gesamtdaten_ideale_funktionen.filter(
                                                                items=['x', 
                                                                funktion_ideal]
                                                                )      
        
                # Tabellen über x mergen       
                join_table = pd.merge(testdaten, data_funktion_ideal, on=["x"],
                                      how="inner")                   
                
                # Abweichungen ermitteln, negative Vorzeichen raus rechnen
                join_table['delta_y'] = (join_table['y'] - join_table[funktion_ideal])**2
                join_table['funkt_nr'] = funktion_ideal       
                       
                # Ergebnis speichern
                ergebnisdaten = pd.concat([ergebnisdaten,join_table[['x','y',
                                                                     'delta_y',
                                                                     'funkt_nr'
                                                                     ]]])        
            
            # Daten auf geringste Abweichung reduzieren 
            
            # Prüfen Wenn Minimum nicht ermittelbar, da nur eine Datenzeile 
            # für x-y-Paar
            if ergebnisdaten[['x','y','delta_y']].groupby(['x','y']).min(
                                                    'delta_y').empty == True:    
                pass
            else:
                ergebnisdaten = pd.merge(
                    ergebnisdaten[['x','y','delta_y']].groupby(['x','y']).min('delta_y'),
                    ergebnisdaten[['x','y','delta_y','funkt_nr']],
                    on=['x','y','delta_y'],how='left'
                )  
             
            
            # Maximale Abweichung Trainingsdaten zu idealer Funktion dazu joinen 
            ergebnisdaten = pd.merge(ergebnisdaten,
                    ideale_passungen[['ideal_funktion','Max_Abweichung']]
                    ,left_on=['funkt_nr'],right_on=['ideal_funktion'],how='left')
            
            #überflüssige Spalte löschen
            ergebnisdaten = ergebnisdaten.drop(columns='ideal_funktion')    
            
            # Löschen Datenzeilen , in denen Abweichung um mehr als Faktor 
            # Wurzel 2 größer als max. Abweichung zwischen Trainingsdaten und 
            # idealer Funktion
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
        else:
            raise ue.DataFrameEmptyError
            
    except ue.DataFrameEmptyError:
        print(ue.DataFrameEmptyError().error_message)