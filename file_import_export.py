'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
from sqlalchemy import create_engine,select,text,MetaData
from os import path
import pandas as pd
import sys

''' Funktion zum Auslesen von Daten aus einer CSV-Datei'''
def read_csv(file):    
    ''' Prüfen, ob Datei im verzeichnis exitiert'''
    if path.exists(file) == True:             
        ''' Daten aus CSV-Datei auslesen und in dataframe speichern '''
        data = pd.read_csv(file,header=0)        
        return data
    else:
        raise FileNotFoundError(f'(data_import) Datei "{file}" nicht im Verzeichnis gefunden.')    
    
        

''' Funktion zum Auslesen von Daten aus einer CSV-Datei und import in eine SQLLite-DB-Tabelle '''
def import_csv_data(file,table,databasename):    
    ''' CSV-Datei einlesen '''
    csv_data = read_csv(file)
    
    ''' Prüfen, ob SQLite-Datenbank-Datei im Verzeichnis exitiert'''
    if path.exists(f'{databasename}.db') == True:    
        '''Mit SQLite-Datenbank verbinden'''
        engine = create_engine(f'sqlite:///{databasename}.db',future = True,echo = True)
       
        ''' Prüfen, ob Daten nicht schon vorhanden sind'''
        con = engine.connect()    
        result = con.execute(text(f'select * from {table}'))
               
        if len(result.all()) == 0:
            csv_data.to_sql(table,con=engine,if_exists='append',index = False,index_label = 'recordid')  
            print(f'(data_import) Daten in Tabelle {table} importiert.\n')
        else:
           raise LookupError(f'(data_import) Es sind bereits Daten in der Tabelle "{table}" vorhanden. Daher werden keine neuen Daten importiert.')
          
    else:
        raise FileNotFoundError(f'(data_import) Datebank-Datei "{databasename}" nicht im Verzeichnis gefunden.')