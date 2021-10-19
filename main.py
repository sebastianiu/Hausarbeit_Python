"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

from database import create_database_model 
from data_processing import data_visualization,read_data,data_import
import pandas as pd


from sqlalchemy.orm import sessionmaker


try:
    '''gewünschter Namen der SQLite-Datenbank deklarieren'''
    
    database='db_hausarbeit_13'  #input('Definieren Sie einen Namen Für die Datenbank, die erzeugt werden muss (Programm mit "-exit" Beenden)')#'db_hausarbeit_13'   
    
    '''SQLite-Datenbank erzeugen'''
    create_database_model(database)
    
    '''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
    data_import('ideal.csv','ideale_funktionen',database)
    data_import('train.csv','trainingsdaten',database)

except:
    print('Fehler ist aufgetreten')

finally:
                                          
    ''' quadratische Abweichungen zwischen trainingsdaten und idealen Funtkionen 
    errechnen und in Dataframe speichern
    '''
    
    ''' Leerer Dataframe für Selektions-Ergebnisse'''
    Tabelle_Ideale_Funktionen_tmp = pd.DataFrame(columns=['train_funktion', 'ideal_funktion', 
                                              'quadr_abw'])
    for i in range(1,5): 
        funktion_train = f'y{i}'
        Selektion_tmp = list()
        for i in range(1,51):        
            funktion_ideal= f'y{i}'        
            
            ''' Daten aus Tabellen auslesen '''
            data_funktion_train = read_data(database,'trainingsdaten','x',funktion_train)
            data_funktion_ideal = read_data(database,'ideale_funktionen','x',funktion_ideal)
            
            #data_funktion_ideal.rename(columns={funktion_ideal:f'funktion_ideal{1}'})
            
            
            ''' Abweichung pro Datenzeile ermitteln und Gesamtsumme aus quadr. Abweichen bilden'''        
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
        
    print('----------Ideale_Funktionen-------'*2)
    print(Tabelle_Ideale_Funktionen_tmp)
    print('-'*20)
    
    
    
    
    ''' Ermittle maximale Abweichung zwischen tainingsdaten und den 4 idealen_Fuktionen'''
    Tabelle_Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 'ideal_funktion', 
                                              'Abweichung'])
    print('----tables----')
    print(tabellennamen(database))
    print('-'*20)
    
    
    
    for i in range(1,2):
          train_funkt = f'y{i}'
          train_data = read_data(database,'trainingsdaten','x',
                                              train_funkt)
          
          ideal_function_data = read_data(database,'ideale_funktionen','x',
                            Tabelle_Ideale_Funktionen_tmp.loc[
                                Tabelle_Ideale_Funktionen_tmp['train_funktion'] == 
                                train_funkt].iloc[0]['ideal_funktion'])
          
          ''' über x joinen '''
          Join_Ergebnistabelle = train_data.join(ideal_function_data.set_index('x'),on='x')
          
          
          ''' Abweichung pro Zeile ermitten '''
          Join_Ergebnistabelle['Abweichung'] = Join_Ergebnistabelle[train_funkt] - \
          Join_Ergebnistabelle[Tabelle_Ideale_Funktionen_tmp.loc[
                                Tabelle_Ideale_Funktionen_tmp['train_funktion'] == 
                                train_funkt].iloc[0]['ideal_funktion']]
         
          
          ''' Datenzeile mit höchster Abweichung hinzufügen    '''  
          Tabelle_Ideale_Funktionen = Tabelle_Ideale_Funktionen.append(
                Join_Ergebnistabelle.loc[Join_Ergebnistabelle['Abweichung'] == 
                                  max(Join_Ergebnistabelle['Abweichung'],['train_funktion',
                                                                   'ideal_funktion', 
                                                                   'Abweichung'])]
                ) 
          
          
    print(Tabelle_Ideale_Funktionen)
          
                                                                                        
 






         















