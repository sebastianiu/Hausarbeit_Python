"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

from data_importer import data_import
from database import create_database_model 
from data_processing import linear_regression_lsquare,data_visualization,read_data
import pandas as pd


from sqlalchemy.orm import sessionmaker

'''gewünschter Namen der SQLite-Datenbank deklarieren'''
database='db_hausarbeit_12'
table='trainingsdaten'


'''SQLite-Datenbank erzeugen'''
#create_database_model(database)

'''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
#data_import('ideal.csv','ideale_funktionen',database)
#data_import('train.csv','trainingsdaten',database)


''' DAten für lineare Regression auslesen '''
data_y1 = read_data(database,table,'x','y1')
data_y2 = read_data(database,table,'x','y2')
data_y3 = read_data(database,table,'x','y3')
data_y4 = read_data(database,table,'x','y4')

''' lineare Regression berechnen'''
lregr_y1= linear_regression_lsquare(data_y1[0],data_y1[1])
lregr_y2= linear_regression_lsquare(data_y2[0],data_y2[1])
lregr_y3= linear_regression_lsquare(data_y3[0],data_y3[1])
lregr_y4= linear_regression_lsquare(data_y4[0],data_y4[1])


''' Prüfen welche idealen Funktion auf berechneten Regressionsgerade liegen '''
''
trainingsdaten = pd.DataFrame(read_data(database, 'trainingsdaten', 'x','y1',
                                        'y1','y3','y4'))

data_ideale_funktionen = pd.DataFrame(read_data(database,'ideale_funktionen',
                                                'x',*[f'y{i}' for i in 
                                                          range(1,51)]
                                                ))


''' quadratische Abweichungen zwischen trainingsdaten und idealen Funtkionen 
errechnen und in Dataframe speichern
'''

''' Leerer Dataframe für Seltkionergebnisse'''
Ideale_Funktionen = pd.DataFrame(columns=['train_funktion', 'ideal_funktion', 
                                          'quadr_abw'])
for i in range(1,5): 
    funktion_train = f'y{i}'
    Selektion_tmp = list()
    for i in range(1,51):        
        funktion_ideal= f'y{i}'
        sum_funktion_train = sum(read_data(database,'trainingsdaten',
                                           funktion_train))
        sum_funktion_ideal = sum(read_data(database,'ideale_funktionen',
                                           funktion_ideal))                
        quadr_abw = sum((sum_funktion_train-sum_funktion_ideal)**2)     
    
        ''' Alle Abweichungen je Trainingsdatenfunktion speichern '''    
        Selektion_tmp.append({'train_funktion':funktion_train,'ideal_funktion':
                              funktion_ideal,'quadr_abw':quadr_abw})     
    
    ''' Minimale Abweichung für y1 - n in Dataframe ermitteln 
    '''
    Selektion_tmp = pd.DataFrame(Selektion_tmp)    
    Ideale_Funktionen = Ideale_Funktionen.append(
            Selektion_tmp.loc[Selektion_tmp['quadr_abw'] == 
                              min(Selektion_tmp['quadr_abw'])]
            )   

print(Ideale_Funktionen)

         
#print('Summe Abweichungen zum Quadrat: ',quadr_abw)





#func_min_qu_abw_y1= min(qu_abw_y1.values)

#print(func_min_qu_abw_y1)

'''
for func,value in qu_abw_y1:
    if value = func_min_qu_abw_y1:
        print(qu_abw_y1[func])
        else:
            continue

'''



#print(data_ideale_funktionen.index)





#data_visualization(data_y1[0],data_y1[1],lregr_y1[0],lregr_y1[1],'y1')
#data_visualization(data_y2[0],data_y2[1],lregr_y2[0],lregr_y2[1],'y2')
#data_visualization(data_y3[0],data_y3[1],lregr_y3[0],lregr_y3[1],'y3')
#data_visualization(data_y4[0],data_y4[1],lregr_y4[0],lregr_y4[1],'y4')













