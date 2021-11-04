'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

# unittest-Modul und eigenes Skript laden
import unittest
from sqlalchemy import create_engine, MetaData,Table,Column,ForeignKey,Integer
from sqlalchemy.orm import declarative_base,relationship
from user_exceptions import DatabaseFileNotFoundError,DatabaseTableEmptyError
import os
from pandas import DataFrame

# zu testendes Programmmodul
import data_processing as dp

# DB zum Testen erzeugen
# Engine-Objekt erzeugen
test_database = 'test_datenbank_123'

#Testdaten erzeugen
trainingsdaten = DataFrame({'x':[15,16,18],'y1':[54,78,57],'y2':[87,97,107]})
checklist_x_values= 15,16,18

daten_ideale_funktionen = DataFrame({'x':[15,16,18],'y10':[55,79,59],
                                     'y15':[80,90,100],'y25':[88,98,108]})

checklist_ideale_funktionen = ['y10','y25']

testdaten = DataFrame({'x':[15,16,18,100],'y':[55,79,200,300]})
checklist_y_values = [55,79,200]

engine = create_engine(f'sqlite:///{test_database}.db',future = True,
                       echo = True)

Base = declarative_base()
        
#Tabellen-Klassen definieren
class testtabelle(Base):
    __tablename__ = 'testtabelle'            
    x = Column(Integer,primary_key=True)
    y1 = Column(Integer)
    y2 = Column(Integer)
     
# Alle Metadaten-Objekte (Tabellen) erzeugen
Base.metadata.create_all(engine) 

# Testdatentabelle mit Daten befüllen
trainingsdaten.to_sql('testtabelle',con=engine,if_exists='append',
                      index = False,index_label = 'recordid')    

class Test_data_processing(unittest.TestCase):                   
    ''' Testfall: Daten aus Tabelle auslesen '''
    def test_read_data(self):        
        data = dp.read_data(test_database,'testtabelle','x')
        # Zeile für Zeile prüfen ob X-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([x in checklist_x_values for x in data['x']]))
        
    ''' Testfall passende ideale Funktion mit least Suqare ermitteln'''    
    def test_get_fits_with_least_square_method(self):
        data = dp.get_fits_with_least_square_method(trainingsdaten,
                                                    daten_ideale_funktionen)
        # Zeile für Zeile prüfen ob X-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([y in checklist_ideale_funktionen for y in \
                             data['ideal_funktion']]))  
        
    ''' Testfall Testdaten validieren'''    
    def test_validate_testdata(self):
        ideale_passungen = dp.get_fits_with_least_square_method(
                                                            trainingsdaten,
                                                            daten_ideale_funktionen)
        
        data = dp.validate_testdata(ideale_passungen,testdaten,daten_ideale_funktionen)
        # Zeile für Zeile prüfen ob X-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([y in checklist_y_values for y in \
                             data['y']]))      
        
       
        
# Skript im unittest-Kontext ausführen
if __name__ == '__main__':
  unittest.main()
 
# Test-Datenbank am Ende wieder löschen
os.remove(f'{test_database}.db')
 