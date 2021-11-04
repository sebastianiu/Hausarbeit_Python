'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
from sqlalchemy import create_engine,select,text,MetaData
from os import path
import pandas as pd
import sys
from user_exceptions import DataFrameEmptyError,DatabaseFileNotFoundError,\
DatabaseTableAlreadyFullError

def read_csv(file): 
    ''' Funktion zum Auslesen von Daten aus einer CSV-Datei'''
    try:
        # Prüfen, ob Datei im verzeichnis exitiert
        if path.exists(file) == True:             
            # Daten aus CSV-Datei auslesen und in dataframe speichern
            data = pd.read_csv(file,header=0)        
            return data
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
                        engine = create_engine(f'sqlite:///{databasename}.db',future = True,echo = True)
                       
                        # Prüfen, ob Daten nicht schon vorhanden sind
                        con = engine.connect()    
                        result = con.execute(text(f'select * from {table}'))
                               
                        if len(result.all()) == 0:                   
                            # Daten importieren
                            data.to_sql(table,con=engine,if_exists='append',index = False,index_label = 'recordid')  
                            print(f'(data_import) Daten in Tabelle {table} importiert.\n')
                        else:
                           raise DatabaseTableAlreadyFullError  
                    except DatabaseTableAlreadyFullError:
                        print(DatabaseTableAlreadyFullError().error_message)
                else:
                    raise DatabaseFileNotFoundError
                    
            except DatabaseFileNotFoundError:
                print(DatabaseFileNotFoundError().error_message)
            else:
                raise DataFrameEmptyError 
            
    except DataFrameEmptyError:
        print(DataFrameEmptyError().error_message)
        