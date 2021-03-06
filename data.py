'''
Programmmodul für die Datenmodell-Erstellung

zur die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
## Module importieren
from sqlalchemy import create_engine,text
import user_exceptions as ue
import pandas as pd
import fnmatch
import numpy as np
import os
import sys

class database:
    '''
    Funktion um eine SQLite-Datenbank/ -Verbindung ,mittels Engine-Objekt
    zu erzeugen
    '''
    def __init__(self):
        self.connection = create_engine('sqlite:///Datenbank\Programmdatenbank.db', 
                                        echo=False)   
       
class data_processing(database):  
    def read_csv(self,file): 
        ''' Funktion zum Auslesen von Daten aus einer CSV-Datei'''
        '''
        data = pd.read_csv(file,header=0)        
        return data
        '''
        try:
            # Prüfen, ob Datei im verzeichnis exitiert
            if os.path.exists(file) == True:   
                # Prüfen, ob es sich um eine CSV-Datei handelt
                try:
                    if file.endswith('csv') == True:
                        # Daten aus CSV-Datei auslesen und in DataFrame speichern
                        data = pd.read_csv(file,header=0)        
                        return data
                    else:                    
                        raise ue.WrongFileFormatError
                except ue.WrongFileFormatError:
                    print(f'(read_csv) {ue.DataFrameEmptyError().error_message}')                
            else:
                raise FileNotFoundError
        except FileNotFoundError:            
            sys.exit(f'(read_csv) Exception: Datei "{file}" nicht im Verzeichnis ' 
                  'gefunden.')
            
    def import_data(self,data,table):           
        ''' Funktion zum Import von Daten eine parallel erzeugte SQLLite-DB-Tabelle ''' 
        try:
            #Prüfen ob gültige Daten übergeben wurden
            if type(data) == pd.DataFrame and data.empty == False: 
                try:
                   #Datenbankverbdinung aufbauen 
                   with self.connection.connect() as con:
                       # Prüfen, ob Tabellen in Datenbank vorhanden sind
                       result = con.execute("SELECT name FROM sqlite_master WHERE"
                                            " type='table'").fetchall()                       
                       if len(result) > 0:
                           # Wenn Tabelle vorhanden, prüfen, ob Zieltabelle existiert
                           table_names  = sorted(list(zip(*result))[0])
                           if table not in table_names:                               
                               # Tabelle nicht vorhanden: neu erzeugen und Daten importieren 
                               data.to_sql(name=table,con=self.connection,
                                           if_exists='fail',index = False,
                                                    index_label = 'recordid')   
                               print(f'(import_data) Daten importiert und Tabelle'
                                     ' "{table}" erzeugt.\n')
                           else:
                               # Tabelle vorhanden: Prüfen, ob diese leer ist
                               result = con.execute(text(f'select * from {table}')) 
                               if len(result.all()) == 0:
                                   #Daten in vorhandene Tabelle importieren
                                   data.to_sql(name=table,con=self.connection,
                                           if_exists='fail',index = False,
                                                    index_label = 'recordid')   
                                   print(f'(import_data) Daten in Tabelle "{table}" '
                                         'importiert.')    
                               else: 
                                   #Fehler: Tabelle existiert und enthält Daten
                                   raise ue.DatabaseTableAlreadyFullError(table)
                       else:
                           # Tabelle nicht vorhanden: neu erzeugen und Daten importieren 
                           data.to_sql(name=table,con=self.connection,
                                           if_exists='fail',index = False,
                                                    index_label = 'recordid')   
                           print(f'(import_data) Daten importiert und Tabelle '
                                 '"{table}" erzeugt.')                                                                    
                except ue.DatabaseTableAlreadyFullError:
                    print(f'(import_data) {ue.DatabaseTableAlreadyFullError(table).error_message}')                  
            else:
                #Fehler: Keien gültigen Daten übergeben
                raise ue.DataFrameEmptyError                
        except ue.DataFrameEmptyError:
            print(f'(import_data) {ue.DataFrameEmptyError().error_message}')            
            
    def read_data(self,table,*columnames):
        ''' Funktion liest Spalten aus einer Datenbanktabelle aus und speichert Inhalt
        in einem DataFrame '''
        try:        
            with self.connection.connect() as con:
                result = con.execute("SELECT name FROM sqlite_master WHERE"
                                     " type='table'").fetchall()
                #Prüfen ob gültige Daten übergeben wurden
                if len(result) > 0:
                    table_names  = sorted(list(zip(*result))[0])
                    #Prüfen, ob Zieltabelle existiert
                    if table in table_names:                             
                        try:                           
                            # Daten aus Tabelle abfragen
                            result = con.execute(text(f'select * from {table}'))
                            # Prüfen, ob auslesbare Daten vorhanden  
                            if len(result.all()) > 0:
                                #Daten auslesen, wenn diese vorhanden sind
                                data = pd.read_sql_table(table,
                                                         self.connection,
                                                        schema=None,
                                                        index_col=None, 
                                                        coerce_float=True, 
                                                        parse_dates=None, 
                                                        columns=(columnames), 
                                                        chunksize=None
                                                        )                    
                                return data                
                            else:
                                #Fehler: Keine auslesbaren Daten vorhanden
                                raise ue.DatabaseTableEmptyError(table)                     
                        except ue.DatabaseTableEmptyError:
                            print(f'(read_data) {ue.DatabaseTableEmptyError(table).error_message}')                      
                    else:
                        #Fehler: Keine auslesbare Datenbanktabelle vorhanden
                        raise ue.DatabaseTableNotExistsError(table)                           
        except ue.DatabaseTableNotExistsError:
            print(f'(read_data) {ue.DatabaseTableNotExistsError(table).error_message}')         
      
           
    def get_fits_with_least_square_method(self,trainingsdaten,daten_ideale_funktionen):    
        ''' Funktion, um die vier besten Passungen zwischen Trainingsdaten und 
        idealen Funktionen mit least suqare Methode zu ermittelt und 
        zusätzliche die maximale Abweichung je idealer Funktion zu den 
        Trainingsdaten speichert        
        '''   
        try:
            # Prüfen, ob Funktionsargumente Daten enthalten
            if type(trainingsdaten) == pd.DataFrame and trainingsdaten.empty == False \
               and type(daten_ideale_funktionen) == pd.DataFrame \
               and daten_ideale_funktionen.empty == False:
                
                # Leerer Dataframe für Selektions-Ergebnisse erzeugen
                Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 
                                                                   'ideal_funktion', 
                                                                    'sum_delta_quadr']
                                                         )           
                              
                # Zwei Listen aller Y-Spalten in Traininsgdaten und idealen 
                # Funktionen erzeugen
                trainingsdaten_y_spalten = fnmatch.filter(trainingsdaten.columns,
                                                          'y*')            
                ideale_funktionen_y_spalten = fnmatch.filter(
                                            daten_ideale_funktionen.columns,'y*')
                
                # passendeste Ideal-Funktion je Trainingsdatensatz ermitteln
                for funktion_train in trainingsdaten_y_spalten:
                    # DataFrame für Zwischenergebnis erzeugen
                    Zwischenergebnis = pd.DataFrame(columns=['train_funktion',
                                                             'ideal_funktion',
                                                            'sum_delta_quadr'])
                    
                    # Summe quadr. Abweichungen zwischen Trainingsdatensatz und 
                    # jeder Ideale-Funktion berechnen
                    for funktion_ideal in ideale_funktionen_y_spalten:                        
                        # Trainingsdatensatz u. Daten Ideal-Funktionen auslesen            
                        data_funktion_train = trainingsdaten.filter(items=['x',
                                                                funktion_train])
                        
                        data_funktion_ideal =daten_ideale_funktionen.filter(
                                                                        items=['x', 
                                                                    funktion_ideal]
                                                                     )          
                                    
                        # Tabellen über x joinen, wenn Spaltennamen gleich, suffix einsetzen                                 
                        if funktion_train == funktion_ideal:
                            join_table= data_funktion_train.join(
                                                    data_funktion_ideal.set_index('x'),
                                                    on='x',rsuffix='_ideal')
                            # Summe aus quadr. Abweichungen ermitteln 
                            quadr_abw =  sum((join_table[funktion_train] - 
                                                 join_table[f'{funktion_ideal}_ideal']
                                                 )**2)
                        else:
                            join_table= data_funktion_train.join(
                                                data_funktion_ideal.set_index('x'),
                                                on='x')
                            
                            quadr_abw =  sum((join_table[funktion_train] - 
                                                join_table[funktion_ideal]
                                              )**2)
                        
                        # Summe Abweichungen je Ideal-Funktion zwischenspeichern
                        Zwischenergebnis = Zwischenergebnis.append({
                                                'train_funktion':funktion_train,
                                                'ideal_funktion': funktion_ideal,
                                                'sum_delta_quadr':quadr_abw},
                                                            ignore_index=True)     
                
                    # Ideal-Funktionen mit minimalster Abweichung zu ermitteln                                    
                    Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                            Zwischenergebnis.loc[
                                            Zwischenergebnis['sum_delta_quadr'] == 
                                           min(Zwischenergebnis['sum_delta_quadr'])]
                            ) 
                                    
                ## maximale Abweichung der Trainingsdaten zu allen 4 ideale Funktionen
                ## ermitteln  
                # leerer DataFrame für Zwischenergebnisse erzeugen
                Zwischenergebnis = pd.DataFrame(columns=['train_funktion','ideal_funktion','delta_quadr'])     
                    
                for funktion_train,funktion_ideal in list(zip(
                                    Tabelle_Ideale_Funktionen['train_funktion'],
                                 Tabelle_Ideale_Funktionen['ideal_funktion'])):
                                          
                    # Trainingsdatensatz u. Daten Ideal-Funktionen auslesen            
                    data_funktion_train = trainingsdaten.filter(items=['x',
                                                                funktion_train])
                    data_funktion_ideal = daten_ideale_funktionen.filter(
                                                                items=['x',
                                                                funktion_ideal]
                                                                )        
                        
                    # Tabellen über x mergen und Delta Y je X-Wert ermitteln                     
                    join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'),
                                                            on='x',rsuffix='_ideal'
                                                                             )
                    join_table['delta_quadr'] =  (join_table[funktion_train] 
                                            - join_table[funktion_ideal])**2
                 
                    # Max. Delta je Paarung Trainingsdaten u. zugehö. Idealfunktion ermitteln
                    Zwischenergebnis = Zwischenergebnis.append(
                                                {
                                                'train_funktion':funktion_train,
                                                'ideal_funktion': funktion_ideal,
                                                'delta_quadr':
                                                join_table['delta_quadr'].loc[
                                                join_table['delta_quadr'] == 
                                        max(join_table['delta_quadr'])].iloc[0]                              
                                                },ignore_index=True
                                                 )     
                       
                # Max. Delta über alle Paarungen ermitteln und an Gesamt-Tabelle anfügen
                Tabelle_Ideale_Funktionen['max_delta_quadr'] = Zwischenergebnis['delta_quadr'].loc[
                    Zwischenergebnis['delta_quadr'] == max(Zwischenergebnis['delta_quadr'])].iloc[0]
                
                print('*** Beste Passungen ***')
                print(Tabelle_Ideale_Funktionen)
                print('\n')
                return Tabelle_Ideale_Funktionen            
            else:
                raise ue.DataFrameEmptyError
        except ue.DataFrameEmptyError:
                print(f'(get_fits_with_least_square_method) {ue.DataFrameEmptyError().error_message}')  
                
    def validate_testdata(self,ideale_passungen,testdaten,gesamtdaten_ideale_funktionen):   
        ''' 
        Funktion um Testdaten zu validieren, d. h. ideale Funktionen ermitteln, die 
        das Kriterium in 2a erfüllen und mit  X-Y-Testdaten, Delta Y und y-Wert pro 
        idealer Funktion in eigene Tabelle schreiben
        '''    
        try:
            # Prüfen, ob alle Funktionsargumente Daten enthalten
            if type(ideale_passungen) == pd.DataFrame \
            and ideale_passungen.empty == False \
            and type(testdaten) == pd.DataFrame and testdaten.empty == False \
            and type(gesamtdaten_ideale_funktionen) == pd.DataFrame \
            and gesamtdaten_ideale_funktionen.empty == False:
                   
            # Maximale Abweichungen zwischen (einer) idealen Funktion und 
            # Testdatensatz ermitteln                
                Liste_validierte_ideale_Funktionen = list() 
                Zwischenergebnis = pd.DataFrame(columns=['x','y','Delta_y','funktion_ideal'])
                           
                for funktion_ideal in list(ideale_passungen['ideal_funktion']): 
                                
                    #Werte Ideal-Funktionen auslesen
                    data_funktion_ideal = gesamtdaten_ideale_funktionen.filter(
                                                    items=['x',funktion_ideal])
                    
                    # Tabellen über x mergen       
                    join_table = pd.merge(testdaten, data_funktion_ideal, on=["x"], 
                                                                      how="inner")                                  
                                
                    # Abweichungen ermitteln
                    join_table['Delta_y'] = (join_table['y'] - join_table[funktion_ideal])**2
                    join_table['funktion_ideal'] = funktion_ideal                      
                         
                    #X-Y-Paarung mit Deltas einzeln temporär speichern
                    Zwischenergebnis = pd.concat([Zwischenergebnis,join_table[
                                        ['x','y','Delta_y','funktion_ideal']
                                    ]]) 
                    
                    # Wenn Max-Delta d. Testdaten zu Ideal < als Max-Detlas*sqrt(2),
                    # dann füge Ideal-Funktion der Liste der vollst. validierten hinzu
                    if join_table['Delta_y'].loc[
                            join_table['Delta_y'] == max(join_table['Delta_y'])
                                   ].iloc[0] < np.sqrt(2) * ideale_passungen['max_delta_quadr'].iloc[0]:
                        Liste_validierte_ideale_Funktionen.append(funktion_ideal)
                    else:
                        continue                     
                    
                # Einzeln gespeicherte Testdaten-Paare auf validierte eingenzen                             
                Testdaten_validiert = Zwischenergebnis.loc[
                                            Zwischenergebnis['Delta_y'] <=  
                                            np.sqrt(2) * ideale_passungen[
                                                'max_delta_quadr'].iloc[0]]                
                            
            if len(Liste_validierte_ideale_Funktionen) < 1:
                print('(validate_testdata) Keine ideale Funktion vollständig'
                      ' validiert!\n')                
                print(f'Anzahl Testdatenpaare validiert: {len(Testdaten_validiert)} von {len(testdaten)}')
                return Testdaten_validiert
                
            else:
                print('(validate_testdata) Folgende Ideal-Funktionen wurde '
                      'vollständig validiert')
                print(Liste_validierte_ideale_Funktionen) 
                print(f'Anzahl Testdatenpaare validiert: {len(Testdaten_validiert)} von {len(testdaten)}')
                return Testdaten_validiert                                       
               
        except ue.DataFrameEmptyError:
            print(f'(validate_testdata) {ue.DataFrameEmptyError().error_message}')     