"""
Programm fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

from data_importer import datenimport
from database import create_database_model 

'''SQLite-Datenbank erzeugen'''
create_database_model('db_hausarbeit')

'''Daten aus CSV auslesen und in Tabellen importieren'''
datenimport('test.csv','testdaten','db_hausarbeit')
datenimport('ideal.csv','ideale_funktionen','db_hausarbeit')
datenimport('train.csv','trainingsdaten','db_hausarbeit')








