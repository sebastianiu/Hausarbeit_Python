"""
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

from data_importer import datenimport
from database import create_database_model 
from data_processing import linear_regression_with_least_square


'''gewünschter Namen der SQLite-Datenbank deklarieren'''
database='db_hausarbeit_3'

'''SQLite-Datenbank erzeugen'''
#create_database_model(database)

'''Trainingsdaten und Daten zu idealen Funtkionen aus CSV auslesen und in Tabellen importieren'''
#datenimport('ideal.csv','ideale_funktionen',database)
#datenimport('train.csv','trainingsdaten',database)

''' lineare Regression '''
linear_regression_with_least_square(database,'trainingsdaten','x','y1')

linear_regression_with_least_square(database,'trainingsdaten','x','y2')

linear_regression_with_least_square(database,'trainingsdaten','x','y3')

linear_regression_with_least_square(database,'trainingsdaten','x','y4')











