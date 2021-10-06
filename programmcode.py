"""
Programm fÃ¼r die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
"""

""" Erfoderliche Paket importieren"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
#import sqlite3
import pandas
import bokeh
import matplotlib

"""Klassen fuer die Tabellenstrukturen """
class testdaten(Table):
    __tablename__ = 'test'
    x = Column(Integer, primary_key=True)
    y1 = Column(Integer)

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'employee'
    }

class trainingsdaten(Employee):
    manager_data = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'manager'
    }

def Datenbank_erzeugen (Datenbanbname):
    engine = create_engine(f'sqlite:///{Datenbanbname}.db', echo = True)
    meta = MetaData()

"""Klassen fuer die Tabellenstrukturen """
class testdatentabelle(Table):
    'testdaten',meta,
    Column('x', Integer), 
    Column('y1', Integer)
 

class trainingsdatentabelle(testdatentabelle):
    'trainingsdaten',meta,
    Column('y2', Integer), 
    Column('y3', Integer),
    Column('y4', Integer)
  

train = testdatentabelle()
test = trainingsdatentabelle()

meta.create_all(engine)
    

    
'''
    'test', meta, 
    Column('id', Integer, primary_key = True), 
    Column('name', String), 
    Column('lastname', String),
    )

'''    
    
'''
 """Klassen fuer die Tabellenstrukturen """
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

'''
    

    

""" Funktion zur Erzegung der Datenbank """
def Datenbank_erzeugen(databasename):

    engine = create_engine('sqlite:///testdaten.db', echo = True)
    meta = MetaData()           


""" Funktion zum  Import der Daten aus CSV-File """
#def Daten_Import ():
    
    
#Datenbank_erzeugen("testdatenank")


    
    
    
    

    

    
    
    

