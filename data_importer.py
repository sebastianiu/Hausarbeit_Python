"""
Programm fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

import pandas as pd
from sqlalchemy import create_engine,select,text
from os import path
import sys

def datenimport(file,table,database): 
    
    ''' Prüfen, ob datei im verzeichnis exitiert'''
    if path.exists(file):    
        '''Mit SQLite-Datenbank verbinden'''
        engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True)   
        
        ''' Daten aus CSV-Dateu auslesen und in dataframe speichern '''
        data = pd.read_csv(file,header=0)    
    
        ''' Prüfen, ob Daten nicht schon vorhanden sind'''
        con = engine.connect()    
        result = con.execute(text(f'select * from {table}'))
               
        if len(result.all()) == 0:
            data.to_sql(table,con=engine,if_exists='append',index = False,index_label = 'recordid')  
            print(f'Daten in Tabelle {table} importiert.\n')
        else:
           print(f'\n!!! Es sind bereits Daten in der Tabelle {table} vorhanden. Daher werden keine neuen Daten importiert. !!!\n')
          
    else:
        print(f'!!! Datei "{file}" nicht im verzeichnis gefunden !!!\n')
          
     
            




