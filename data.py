'''
Programmmodul für die Datenmodell-Erstellung

zur die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base,relationship
import user_exceptions as ue
import pandas as pd
import fnmatch
import numpy as np
import os

class database:
    '''
    Funktion um eine SQLite-Datenbank/ -Verbindung ,mittels Engine-Objekt
    zu erzeugen
    '''
    def __init__(self):
        self.connection = create_engine('sqlite:///Datenbank\Programmdatenbank.db', echo=False)   
       
class data_processing(database):    
    def import_data(self,data,table):           
        ''' 
        Funktion zum Import von Daten eine parallel erzeugte SQLLite-DB-Tabelle  
        ''' 
        try:
            if data.empty == False: 
                try:
                   # Prüfen, ob Daten nicht schon vorhanden sind
                   with self.connection.connect() as con:
                       result = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                       table_names  = sorted(list(zip(*result))[0])
                       if table not in table_names:
                           # Daten importieren und Tabelle neu erzeugen
                           data.to_sql(name=table,con=self.connection,
                                       if_exists='fail',index = False,
                                                index_label = 'recordid')   
                           print(f'(import_data) Daten importiert und Tabelle '
                                 '{table} erzeugt.\n')
                       else:
                           result = con.execute(text(f'select * from {table}')) 
                           if len(result.all()) == 0:
                               #Daten in existente Tabelle importieren
                               data.to_sql(name=table,con=self.connection,
                                       if_exists='fail',index = False,
                                                index_label = 'recordid')   
                               print(f"(import_data) Daten in Tabelle '{table}' importiert.\n")    
                           else: 
                               #Fehler: Tabelle existiert und enhtält Daten
                               raise ue.DatabaseTableAlreadyFullError(table)  
                except ue.DatabaseTableAlreadyFullError:
                    print(f'(import_data) {ue.DatabaseTableAlreadyFullError(table).error_message}')                  
            else:
                raise ue.DataFrameEmptyError                
        except ue.DataFrameEmptyError:
            print(f'(import_data) {ue.DataFrameEmptyError().error_message}')
            
            
    def read_data(self,table,*columnames):
        '''
        Funktion liest Spalten aus einer Datenbanktabelle aus und speichert Inhalt
        in einem DataFrame        
        '''
        try:        
            with self.connection.connect() as con:
                result = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                table_names  = sorted(list(zip(*result))[0])
                #Prüfen, ob Zieltabelle existiert
                if table in table_names:  
                    # Prüfen, ob auslesbare Daten vorhanden        
                    try:
                        #with self.connection.connect() as con:
                        # Daten aus Tabelle abfragen
                        result = con.execute(text(f'select * from {table}'))
                        if len(result.all()) > 0:
                            #Daten auslesen, wenn diese vorhanden sind
                            data = pd.read_sql_table(table,self.connection,
                                                         schema=None,index_col=None, 
                                                    coerce_float=True, parse_dates=None, 
                                                    columns=(columnames), chunksize=None
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
            print(f'(read_csv) Exception: Datei "{file}" nicht im Verzeichnis gefunden.') 
           
    def get_fits_with_least_square_method(self,trainingsdaten,daten_ideale_funktionen):    
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
                Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 
                                                                   'ideal_funktion', 
                                                                    'quadr_abw']
                                                         )           
                              
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
                    
                    Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                            Selektion_tmp.loc[
                                            Selektion_tmp['quadr_abw'] == 
                                           min(Selektion_tmp['quadr_abw'])]
                            ) 
                                    
                ## maximale Abweichung der Trainingsdaten zu allen 4 ideale Funktionen
                ## ermitteln    
                 
                # leerer DataFrame für Zwischenergebnisse erzeugen
                Zwischenergebnis = pd.DataFrame(columns=['train_funktion','ideal_funktion','quadr_abw'])     
                    
                #for funktion_train in trainingsdaten_y_spalten:
                for funktion_train,funktion_ideal in list(zip(Tabelle_Ideale_Funktionen['train_funktion'],
                                                              Tabelle_Ideale_Funktionen['ideal_funktion'])):
                                          
                    # Daten auslesen            
                    data_funktion_train = trainingsdaten.filter(items=['x',funktion_train])
                    data_funktion_ideal = daten_ideale_funktionen.filter(items=['x',funktion_ideal])        
                        
                    # Tabellen joinen und Abweichung pro Datenzeile ermitteln 
                    #und Gesamtsumme aus quadr. Abweichen bilden  
                    join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'),
                                                            on='x',rsuffix='_ideal'
                                                                             )
                    join_table['quadr_abw'] =  (join_table[funktion_train] - join_table[funktion_ideal])**2
                 
                    
                    Zwischenergebnis = Zwischenergebnis.append(
                                                {
                                                'train_funktion':funktion_train,
                                                'ideal_funktion': funktion_ideal,
                                                'quadr_abw':join_table['quadr_abw'].loc[
                                                    join_table['quadr_abw'] == max(join_table['quadr_abw'])].iloc[0]                              
                                                },ignore_index=True
                                                 )     
                       
                #Maximale_Abweichung zwischen allen 4 Trainingsdaten u. zugeh. ideal. Funkt. anfügen   
                Tabelle_Ideale_Funktionen['Max_Delta'] = Zwischenergebnis['quadr_abw'].loc[
                    Zwischenergebnis['quadr_abw'] == max(Zwischenergebnis['quadr_abw'])].iloc[0]
                
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
        Funktion um Testdaten zu validieren, d. h. ideale Funktionen ermitten, die 
        das Kriterium in 2a erfüllen und mit  X-Y-Testdaten, Delta Y und y-Wert pro 
        idealer Funktion in eigene Tabelle schreiben
        '''    
        try:
            # Prüfen, ob alle Funktionsargumente Daten enthalten
            if ideale_passungen.empty == False \
            and testdaten.empty == False  \
            and gesamtdaten_ideale_funktionen.empty == False:
                   
            # Maximale Abweichungen zwischen (einer) idealen Funktion und 
            # Testdatensatz ermitteln
                
                Liste_validierte_ideale_Funktionen = list()            
                Ergebnisdaten = pd.DataFrame(columns=['ideal_funktion','Max_Abweichung'])              
                           
                #for i in range(0,len(ideale_passungen)):  
                for funktion_ideal in list(ideale_passungen['ideal_funktion']):      
                                                       
                    # Werte der idealen funktion auslesen
                    # funktion_ideal = ideale_passungen.loc[i].at['ideal_funktion']
                                
                    # Trainingsdaten auslesen
                    data_funktion_ideal = gesamtdaten_ideale_funktionen.filter(
                                                        items=['x',funktion_ideal]
                                                                                )
                    
                    # Tabellen über x mergen       
                    join_table = pd.merge(testdaten, data_funktion_ideal, on=["x"], 
                                                                      how="inner")                                  
                                
                    #Abweichungen ermitteln
                    join_table['Delta_y'] = (join_table['y'] - join_table[funktion_ideal])**2
                    
                    #TEST
                    join_table.to_csv('delta_testdaten.csv')
                                  
                    Max_Abweichung = join_table[
                    'Delta_y'].loc[join_table['Delta_y'] == max(join_table['Delta_y'])
                                   ].iloc[0]   
                            
                    Ergebnisdaten = Ergebnisdaten.append({'ideal_funktion': funktion_ideal,
                                         'Max_Abweichung': Max_Abweichung
                                        },ignore_index=True)         
                    
                    #Wenn Max_Abweichung M < als N*sqrt(2), dann füge Ideal-Funktion
                    # der Liste der validierten hinzu
                    if Max_Abweichung < np.sqrt(2) * ideale_passungen['Max_Delta'].iloc[0]:
                        Liste_validierte_ideale_Funktionen.append(funktion_ideal)
                    else:
                        continue
                    
                    
                #Pro validierter Idealfunktion Tabelle erzeugen, die X,Y (Testdaten)
                # und quadratische Abweichung Sowie Y-Wert der ideal-Funtkion 
                # als Spalte enthält                
                
                if len(Liste_validierte_ideale_Funktionen) > 0:                
                    for Ideal_Funktion_validiert in Liste_validierte_ideale_Funktionen:
                        
                            #Tabellenname erzeugen
                            table = f'Testdaten_zu_{Ideal_Funktion_validiert}'
                        
                        
                            #leere DataFrame für Ergebnisse
                            Ergebnisdaten = pd.DataFrame(columns=['X','Y','Delta Y',Ideal_Funktion_validiert])  
                            
                            # Daten laden
                            data_funktion_ideal = gesamtdaten_ideale_funktionen.filter(
                                                            items=['x',Ideal_Funktion_validiert]
                                                                                           )
                            # Tabellen über x mergen       
                            join_table = pd.merge(testdaten, data_funktion_ideal, on=["x"], 
                                                                          how="inner")
                            
                            #Abweichungen ermitteln
                            join_table['Delta y'] = (join_table['y'] - join_table[Ideal_Funktion_validiert])**2

                            # Daten in Tabelle speichern
                            try:
                                # Prüfen, ob Daten nicht schon vorhanden sind                        
                                with self.connection.connect() as con:
                                   result = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                                   table_names  = sorted(list(zip(*result))[0])
                                   if table not in table_names:
                                       # Daten importieren und Tabelle neu erzeugen
                                        join_table.to_sql(name=table,con=self.connection,
                                                   if_exists='fail',index = False,
                                                            index_label = 'recordid')  
                                        print(f'(validate_testdata) Daten importiert und Tabelle {table} erzeugt.')
                                   else:
                                       result = con.execute(text(f'select * from {table}')) 
                                       if len(result.all()) == 0:
                                           #Daten in existente Tabelle importieren
                                           join_table.to_sql(name=table,con=self.connection,
                                                   if_exists='fail',index = False,
                                                            index_label = 'recordid')   
                                           print(f'(validate_testdata) Daten in Tabelle "{table}" importiert.')    
                                       else: 
                                           #Fehler: Tabelle existiert und enhtält Daten
                                           raise ue.DatabaseTableAlreadyFullError(table)  
                            except ue.DatabaseTableAlreadyFullError:
                                print(f'(validate_testdata) {ue.DatabaseTableAlreadyFullError(table).error_message}')  
                            
                    return Liste_validierte_ideale_Funktionen 
                
                    print(f'*** ideale Funktionen durch Testdaten valdiert ***')
                    print(Liste_validierte_ideale_Funktionen)
                       
                else:
                    print('(validate_testdata) Keine ideale Funktion validiert !!') 
                    print('*** Abweichungen zu Testdaten ***')
                    print(Ergebnisdaten)
            else:
                raise ue.DataFrameEmptyError                
               
        except ue.DataFrameEmptyError:
            print(f'(validate_testdata) {ue.DataFrameEmptyError().error_message}')  
                
                        
           

    
       
        

