# -*- coding: utf-8 -*-
'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

'''erfoderliche Pakete importieren'''
import numpy as np
import pandas as pd
from sqlalchemy import create_engine,select,text,MetaData
from sqlalchemy.orm import declarative_base
from os import path
import sys




def data_import(file,table,databasename):     
    
    ''' Funktion zum Auslesen von Daten aus einer CSV-Datei und import in eine SQLLite-DB-Tabelle '''
    ''' Prüfen, ob datei im verzeichnis exitiert'''
    if path.exists(file):    
        '''Mit SQLite-Datenbank verbinden'''
        engine = create_engine(f'sqlite:///{databasename}.db',future = True,echo = True)   
         
        ''' Daten aus CSV-Dateu auslesen und in dataframe speichern '''
        data = pd.read_csv(file,header=0)    
    
        ''' Prüfen, ob Daten nicht schon vorhanden sind'''
        con = engine.connect()    
        result = con.execute(text(f'select * from {table}'))
               
        if len(result.all()) == 0:
            data.to_sql(table,con=engine,if_exists='append',index = False,index_label = 'recordid')  
            print(f'(data_import) Daten in Tabelle {table} importiert.\n')
        else:
           raise LookupError(f'(data_import) Es sind bereits Daten in der Tabelle "{table}" vorhanden. Daher werden keine neuen Daten importiert.')
          
    else:
        raise FileNotFoundError(f'(data_import) Datei "{file}" nicht im Verzeichnis gefunden.')



def tabellennamen(database):#columnname_1,columnname_2):
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect()   


'''Funktion liest Spalten aus einer Datenbanktabelle aus'''
def read_data(database,table,*columnames):#columnname_1,columnname_2):
    '''Mit SQLite-Datenbank verbinden'''
    engine = create_engine(f'sqlite:///{database}.db',future = True,echo = True) 
    
    ''' Daten aus Tabelle auslesen'''
    con = engine.connect() 
    
    result = con.execute(text(f'select * from {table}'))
        
    ''' Prüfen, ob auslesbare Daten vorhanden'''             
    if len(result.all()) == 0:
         raise LookupError(f'(read_data) Tabelle "{table}" enthält keine Daten!')
    else:
        data = pd.read_sql_table(table, con, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=(columnames), chunksize=None)#(columnname_1,columnname_2), chunksize=None)
                    
        return data
''' Funktion ermittelt Formel für Regressionsgerade mit least-Square-Methodik'''
def linear_regression_lsquare(X,Y):      
    
    ''' Ermittle a und b für Trendgeraden-Formel y= a+b* x '''    
    ''' arithmn mitte für x und y berechnen'''    
    mean_x = np.mean(X)
    mean_y = np.mean(Y)
     
    ''' Gesamtzahl der x-Werte''' 
    n = len(X)
    
    ''' Werte zur Berechnung von b ermitteln'''
    Zaehler = 0
    Nenner = 0
    
    ''' Berechnung über alle Datenzeilen'''
    for i in range(n):
        Zaehler += (X[i] - mean_x) * (Y[i] - mean_y)
        Nenner += (X[i] -  mean_x) ** 2
        
    ''' Berechne a und b'''
    b = Zaehler / Nenner
    a = mean_y - (b * mean_x)   
    
    return [a,b]

 
''' Funktion um die 4 besten Passungen zwischen Trainingsdaten und idealen 
Funktionen mit least suqare Methode zu ermitteln
'''
def get_fits_with_least_square_method(database,tablename_traindata = 'trainingsdaten'
                                      ,tablename_idealfunctions = 'ideale_funktionen'):
    
    ''' Leerer Dataframe für Selektions-Ergebnisse'''
    Tabelle_Ideale_Funktionen_tmp = pd.DataFrame(columns=['train_funktion', 'ideal_funktion', 
                                              'quadr_abw'])
    
    '''quadr. Abweichungen zwischen Trainingsdaten und idealen Funktionen ermitteln '''
    for i in range(1,5): 
        funktion_train = f'y{i}'
        Selektion_tmp = list()
        
        for i in range(1,51):        
            funktion_ideal= f'y{i}'        
            
            ''' Daten aus Tabellen auslesen '''
            data_funktion_train = read_data(database,'trainingsdaten','x',funktion_train)
            data_funktion_ideal = read_data(database,'ideale_funktionen','x',funktion_ideal)
            
            #data_funktion_ideal.rename(columns={funktion_ideal:f'funktion_ideal{1}'})
            
            
            ''' Tabellen joinen und Abweichung pro Datenzeile ermitteln und 
            Gesamtsumme aus quadr. Abweichen bilden'''        
            if funktion_train == funktion_ideal:
                join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'),
                                                     on='x',rsuffix='_ideal')
                quadr_abw =  sum((join_table[funktion_train] - 
                                  join_table[f'{funktion_ideal}_ideal'])**2)
            else:
                join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'), on='x')
                quadr_abw =  sum((join_table[funktion_train] - join_table[funktion_ideal])**2)
            
            """ Alle Abweichungen je Trainingsdatenfunktion speichern """
            Selektion_tmp.append({'train_funktion':funktion_train,'ideal_funktion':
                                  funktion_ideal,'quadr_abw':quadr_abw})     
        
        """ Ideale Funktionen mit mit minimalster Abweichung ermitteln   """
        Selektion_tmp = pd.DataFrame(Selektion_tmp)
        
        Tabelle_Ideale_Funktionen_tmp = Tabelle_Ideale_Funktionen_tmp.append(
                Selektion_tmp.loc[
                                Selektion_tmp['quadr_abw'] == 
                               min(Selektion_tmp['quadr_abw'])]
                ) 

    ''' 
    Ermittle maximale Abweichung zwischen tainingsdaten und für jede der 4 
    idealen Funktionen
    '''
    Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 'ideal_funktion', 
                                              'Max_Abweichung'])     
   
    for i in range(1,5):
          funktion_train = f'y{i}'
          data_train = read_data(database,'trainingsdaten','x',funktion_train)
          
          funktion_ideal = Tabelle_Ideale_Funktionen_tmp.loc[
                                Tabelle_Ideale_Funktionen_tmp['train_funktion'] 
                                == funktion_train].iloc[0]['ideal_funktion']
          
          data_funktion_data = read_data(database,'ideale_funktionen','x',
                            funktion_ideal)
          
          ''' Tabellen joinen und Abweichungen pro Datenzeile ermitteln'''        
          if funktion_train == funktion_ideal:
             
              join_table = pd.merge(data_train, data_funktion_data, on="x", 
                                    how="left",rsuffix='_ideal')
                                                     
              ''' Abweichung pro Zeile ermitteln '''
              join_table['Abweichung'] = join_table[funktion_train] - \
                                          join_table[f'{funktion_ideal}_ideal']
               
          else:
              join_table= pd.merge(data_train, data_funktion_data, on="x", how="left")
                       
              ''' Abweichung pro Zeile ermitten '''
              join_table['Abweichung'] = join_table[funktion_train] - \
                                          join_table[funktion_ideal]
         
          '''Zeile mit höchster Abweichung selektieren und in Dataframe speichern  '''
          Max_Abweichung =  join_table.loc[join_table['Abweichung'] == 
                               max(join_table['Abweichung'])].iloc[0]['Abweichung']
          
          Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                                              {
                                              'train_funktion':funktion_train,
                                              'ideal_funktion':funktion_ideal,
                                              'Max_Abweichung':Max_Abweichung
                                              },ignore_index=True)         
         
    return Tabelle_Ideale_Funktionen       
   

def finding_fits(table1,table2):
    '''
    Funktion zur Ermittlung der vier besten Passungen aus Trainingsdaten 
    und idealen Funktionen durch Minimierung der quadratischen Abweichungen
    '''
    pass

''' Daten für lineare Regression auslesen '''
#data_y1 = read_data(database,table,'x','y1')
#data_y2 = read_data(database,table,'x','y2')
#data_y3 = read_data(database,table,'x','y3')
#data_y4 = read_data(database,table,'x','y4')

''' lineare Regression berechnen'''
#lregr_y1= linear_regression_lsquare(data_y1[0],data_y1[1])
#lregr_y2= linear_regression_lsquare(data_y2[0],data_y2[1])
#lregr_y3= linear_regression_lsquare(data_y3[0],data_y3[1])
#lregr_y4= linear_regression_lsquare(data_y4[0],data_y4[1])

#data_visualization(data_y1[0],data_y1[1],lregr_y1[0],lregr_y1[1],'y1')
#data_visualization(data_y2[0],data_y2[1],lregr_y2[0],lregr_y2[1],'y2')
#data_visualization(data_y3[0],data_y3[1],lregr_y3[0],lregr_y3[1],'y3')
#data_visualization(data_y4[0],data_y4[1],lregr_y4[0],lregr_y4[1],'y4')
