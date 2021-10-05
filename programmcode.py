"""
Programm fÃ¼r die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

""" Erfoderliche Paket importieren"""
import sqlalchemy
import sqlite3
import pandas
import bokeh
import matplotlib

"""Klassen fÃ¼r die Tabellenstrukturen """
class test():
    def __init__(self, x,y1):
        self.x = x
        self.y1 = x
 
""" Definieren weitere Tabellenklassen, die von test erben """        
class train(test):
    def __init__(self,x,y1,y2,y3,y4):
        """ Konstruktor-Methode der Elternklasse ausführen """
        test.__init__(self,x,y1)      
        """ angepasste Konstruktor-Methode der Kind-Klasse ausführen  """
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4        
     
class ergebnis(test):
    def __init__(self,x,y1,delta_y,nr_ideal):
        """ Konstruktor-Methode der Elternklasse ausführen """
        test.__init__(self,x,y1)      
        """ angepasste Konstruktor-Methode der Kind-Klasse ausführen  """
        self.delta_y = delta_y
        self.nr_ideal = nr_ideal

""" Definiere Klasse für Tabelle der idealen Funktionen  """
class ideal(test):
    pass
 
"""  Ergänze Attribute y2 bis y50 """
for i in range(2,51):
    setattr(ideal,f'y{i}',f'y{i}')
    



        

""" Funktion zur Erzegung der Datenbank """
def Datenbank_erzeugen(databasename):

    database = databasename
    connection = sqlite3.connect(f'{database}.db')
    cursor = connection.cursor()       
       
    """ Tabellen erzeugen """
    command1 = '''CREATE TABLE IF NOT EXISTS Test
                (x1 INT, y1 INT)
            '''  
       
    cursor.execute(command1)
    
    connection.close()


""" Funktion zum  Import der Daten aus CSV-File """
#def Daten_Import ():
    
    
#Datenbank_erzeugen("testdatenank")


    
    
    
    

    

    
    
    

