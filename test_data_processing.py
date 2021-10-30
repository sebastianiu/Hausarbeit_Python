'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

# unittest-Modul und eigenes Skript laden
import unittest
from sqlalchemy import create_engine, MetaData,Table,Column,ForeignKey,Integer
from sqlalchemy.orm import declarative_base,relationship
from exceptions import DatabaseFileNotFoundError,DatabaseTableEmptyError
import os
from pandas import DataFrame

# zu testendes Programmmodul
import data_processing as dp

# DB zum Testen erzeugen
# Engine-Objekt erzeugen
test_database = 'test_datenbank_123'
daten = {'x':[15,16,18],'y':[54,78,57]}
checklist_x_values= 15,16,18
testdaten = DataFrame(daten)

engine = create_engine(f'sqlite:///{test_database}.db',future = True,echo = True)     
Base = declarative_base()
        
#Tabellen-Klassen definieren
class testtabelle(Base):
    __tablename__ = 'testtabelle'            
    x = Column(Integer,primary_key=True)
    y = Column(Integer)
     
# Alle Metadaten-Objekte (Tabellen) erzeugen
Base.metadata.create_all(engine) 

# Testdatentabelle mit Daten befüllen
testdaten.to_sql('testtabelle',con=engine,if_exists='append',index = False,index_label = 'recordid')    

''' Testklasse für das modul data_processing, die die TestCases von unittest 
erbt 
'''

class Test_data_processing(unittest.TestCase):               
    #   Testfall: Daten aus Tabelle auslesen
    def test_read_data(self):        
        data = dp.read_data(test_database,'testtabelle','x')
        self.assertTrue(all([x in checklist_x_values for x in data['x']]))
        
# Skript im unittest-Kontext ausführen
if __name__ == '__main__':
  unittest.main()
 
# Test-Datenbank an Ende wieder löschen
os.remove('test_datenbank_123.db')
 