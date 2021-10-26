# -*- coding: utf-8 -*-
'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit 
Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

'''erfoderliche Pakete importieren'''
from sqlalchemy import create_engine,select,text,MetaData
from sqlalchemy.orm import declarative_base
from os import path
import sys
import numpy as np
import pandas as pd

  
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
        data = pd.read_sql_table(
                                table, con, schema=None, index_col=None, 
                                 coerce_float=True, parse_dates=None, 
                                 columns=(columnames), chunksize=None
                                 )                   
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
    Tabelle_Ideale_Funktionen_tmp = pd.DataFrame(columns=[
                                                            'train_funktion', 
                                                            'ideal_funktion', 
                                                            'quadr_abw']
        )
    
    '''quadr. Abweichungen zwischen Trainingsdaten und idealen Funktionen ermitteln '''
    for i in range(1,5): 
        funktion_train = f'y{i}'
        Selektion_tmp = list()
        
        for i in range(1,51):        
            funktion_ideal= f'y{i}'        
            
            ''' Daten aus Tabellen auslesen '''
            data_funktion_train = read_data(database,'trainingsdaten','x',funktion_train)
            
            data_funktion_ideal = read_data(database,'ideale_funktionen','x',funktion_ideal)
            
            ''' Tabellen joinen und Abweichung pro Datenzeile ermitteln und 
            Gesamtsumme aus quadr. Abweichen bilden'''        
            if funktion_train == funktion_ideal:
                join_table= data_funktion_train.join(data_funktion_ideal.set_index('x'),
                                                     on='x',rsuffix='_ideal')
                quadr_abw =  sum((join_table[funktion_train] - 
                                  join_table[f'{funktion_ideal}_ideal'])**2)
            else:
                join_table= data_funktion_train.join(
                                data_funktion_ideal.set_index('x'),on='x'
                                    )
                quadr_abw =  sum(
                                (
                                    join_table[funktion_train] - 
                                    join_table[funktion_ideal]
                                  )**2
                                )
            
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
    Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 
                                                      'ideal_funktion', 
                                              'Max_Abweichung'])     
   
    for i in range(1,5):
          funktion_train = f'y{i}'
          trainingsdaten = read_data(database,'trainingsdaten','x',funktion_train)
          
          funktion_ideal = Tabelle_Ideale_Funktionen_tmp.loc[
                                Tabelle_Ideale_Funktionen_tmp['train_funktion'] 
                                == funktion_train].iloc[0]['ideal_funktion']
          
          daten_ideale_funktionen = read_data(database,'ideale_funktionen','x',
                            funktion_ideal)
          
          ''' Tabellen joinen und Abweichungen pro Datenzeile ermitteln'''        
          if funktion_train == funktion_ideal:
             
              join_table = pd.merge(trainingsdaten, daten_ideale_funktionen, on="x", 
                                    how="left",rsuffix='_ideal')
                                                     
              ''' Abweichung pro Zeile ermitteln '''
              join_table['Abweichung'] = join_table[funktion_train] - \
                                          join_table[f'{funktion_ideal}_ideal']
               
          else:
              join_table= pd.merge(trainingsdaten, daten_ideale_funktionen, 
                                   on="x", how="left")
                       
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
   
''' 
Funktion um Testdaten zu validieren: x-Y-Paare zu selektieren, die das Kriterium 
in U-Abschnitt 2 erfüllen

'''
def validate_testdata(data_ideal_fits,test_data,database):        
    
    ''' Leerer DataFrame für Ergebnisse erzeugen '''
    ergebnisdaten = pd.DataFrame(columns=['x','y','delta_y','funkt_nr'])                           
                            
    ''' Abweichungen aller x,y-Paare aus Testdaten zu y-Werten der idealen 
    Funktion ermitteln
    '''
    for i in range(0,4):        
        
        ''' Differenzen der Testwerte zu den idealen funktion ermitteln'''
        funktion_ideal = data_ideal_fits.loc[i].at['ideal_funktion']
        
        daten_ideale_funktion = read_data(database,'ideale_funktionen','x',funktion_ideal) 

        ''' Tabellen über x mergen'''        
        join_table = pd.merge(test_data, daten_ideale_funktion, on=["x"],how="inner")                   
        
        ''' Abweichungen ermitteln, negative Vorzeichen raus rechnen'''
        join_table['delta_y'] = abs(join_table['y']-  join_table[funktion_ideal])
        join_table['funkt_nr']= funktion_ideal       
               
        ''' Ergebnis speichern '''
        ergebnisdaten = pd.concat([ergebnisdaten,join_table[['x','y','delta_y','funkt_nr']]])        
    
    ''' Daten auf geringste Abweichung reduzieren '''    
    ergebnisdaten = pd.merge(
                            ergebnisdaten[['x','y','delta_y',]].groupby(['x','y']).min('delta_y'),
                             ergebnisdaten[['x','y','delta_y','funkt_nr']],
                             on=['x','y','delta_y'],how='left'
                             )    
    ''' Mximale Abweichung Trainingsdaten zu idealer Funktion dazu joinen '''
    ergebnisdaten = pd.merge(ergebnisdaten,
                             data_ideal_fits[['ideal_funktion','Max_Abweichung']]
                             ,left_on=['funkt_nr'],right_on=['ideal_funktion'],how='left')
    
    ergebnisdaten = ergebnisdaten.drop(columns='ideal_funktion')
    
    ''' 
    Löschen Datenzeilen , in denen Abweichung um mehr als Faktor Wurzel 2 größer 
    als max. Abweichung zwischen Trainingsdaten und idealer Funktion
    '''       
    ergebnisdaten.drop(ergebnisdaten[                                                                            
                                        (          
                                        ergebnisdaten['delta_y'] / 
                                        ergebnisdaten['Max_Abweichung']
                                        )  > np.sqrt(2)
                                    ].index, inplace=True                                     
                                     )
    
    ergebnisdaten = ergebnisdaten.drop(columns='Max_Abweichung')
    
    return ergebnisdaten
