'''
Programmmodul für Tests

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

# unittest-Modul und eigenes Skript laden
import unittest
import sqlalchemy as sl
import sqlalchemy.orm as slo
import os
import pandas as pd

# zu testende Programmmodule
import data as db
#import database as db


'''
# DB zum Testen erzeugen
# Engine-Objekt erzeugen
test_database = 'test_datenbank_123'
test_database2 = 'test_datenbank_124'

#Testdatenbank erzeugen
engine = sl.create_engine(f'sqlite:///{test_database}.db',future = True,
                       echo = True)
Base = slo.declarative_base()
        
#Tabellen-Klassen definieren
class testtabelle(Base):
    __tablename__ = 'testtabelle'            
    x = sl.Column(sl.Integer,primary_key=True)
    y1 = sl.Column(sl.Integer)
    y2 = sl.Column(sl.Integer)
     
# Alle Metadaten-Objekte (Tabellen) erzeugen
Base.metadata.create_all(engine) 

'''

#Testdaten erzeugen
trainingsdaten = pd.DataFrame({'x':[15,16,18],'y1':[54,78,57],'y2':[87,97,107]})

#Leerer DataFrame für Gegentest
trainingsdaten2 = pd.DataFrame(columns=['x','y','delta_y','funkt_nr']) 

checklist_trainingsdaten_x_values= 15,16,18

daten_ideale_funktionen = pd.DataFrame({'x':[15,16,18],'y10':[55,79,59],
                                     'y15':[80,90,100],'y25':[88,98,108]})

checklist_ideale_funktionen = ['y10','y25']

testdaten = pd.DataFrame({'x':[15,16,18,100],'y':[55,79,200,300]})
checklist_testdaten_y_values = [55,79,200]

  
  
class Test_data(unittest.TestCase):      
    # Testfall: Datenbank erstellen 
    def __init__(self):
        self.connection = sl.create_engine('sqlite:///Test_Programmdatenbank.db', echo=False)
        
    # Testfall: Daten in Tabelle importieren 
    def test_import_data(self):        
        db.import_data(trainingsdaten,'testtabelle')
        with self.connection.connect() as con:
            # Daten aus Tabelle abfragen
            result = self.connection.execute(sl.text(f'select * from testtabelle'))         
            # Prüfen, ob Daten in Tabelle vorhanden sind
            self.assertTrue(len(result.all()) > 0)   


'''
    
class Test_data_processing(unittest.TestCase):       
    
    
    # Testfall: Daten in Tabelle importieren 
    def test_import_data(self):        
        db.import_data(trainingsdaten,'testtabelle',test_database)
        with engine.connect() as con:
            # Daten aus Tabelle abfragen
            result = con.execute(sl.text(f'select * from testtabelle'))         
            # Prüfen, ob Daten in Tabelle vorhanden sind
            self.assertTrue(len(result.all()) > 0)         
                 
    # Testfall: Daten aus Tabelle auslesen 
    def test_read_data(self):        
        data = db.read_data(test_database,'testtabelle','x')        
        # Zeile für Zeile prüfen ob X-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([x in checklist_trainingsdaten_x_values for x in data['x']]))        
        
    # Testfall passende ideale Funktion mit least Suqare ermitteln    
    def test_get_fits_with_least_square_method(self):
        data = db.get_fits_with_least_square_method(trainingsdaten,
                                                    daten_ideale_funktionen)
        # Zeile für Zeile prüfen ob X-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([y in checklist_ideale_funktionen for y in \
                             data['ideal_funktion']]))              
        
    # Testfall Testdaten validieren    
    def test_validate_testdata(self):
        ideale_passungen = db.get_fits_with_least_square_method(trainingsdaten,
                                                       daten_ideale_funktionen)        
        data = db.validate_testdata(ideale_passungen,testdaten,
                                                       daten_ideale_funktionen)        
        # Zeile für Zeile prüfen ob y-Wert mit Checkliste übereinstimmt
        self.assertTrue(all([y in checklist_testdaten_y_values for y in data['y']]))       
            


class Test_database(unittest.TestCase):                   
        # Testfall: Datenbank erstellen 
        def test_create_database_model(self):        
            data = db.create_database_model(test_database2)        
            # prüfen ob erzeugte Datenbankdatei im filesystem existiert
            self.assertTrue(os.path.exists(f'{test_database2}.db'))

'''

  
        
# Skript im unittest-Kontext ausführen
if __name__ == '__main__':
    unittest.main()
 
    
# Test-Datenbanken wieder löschen
if os.path.exists('Test_Programmdatenbank.db'):
    os.remove('Test_Programmdatenbank.db')
    print('!!Testdatenbank wieder gelöscht!!')
else:
    print('!!Testdatenbank exiastiert nicht!!')
    

'''
if os.path.exists(f'{test_database2}.db'):
    os.remove(f'{test_database2}.db')
    
'''
    

 