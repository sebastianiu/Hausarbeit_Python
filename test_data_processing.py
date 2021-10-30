'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

# unittest-Modul und eigenes Skript laden
import unittest
import data_processing
from database import create_database_model
from datetime import datetime


# DB zum Testen erzeugen
test_database = 'testdatenbank'
create_database_model(test_database)

falsche_database= '###.db'
falsche_tabelle = '###'
falsche_spalten = ['?','?','?']

''' Testklasse für das modul data_processing, die die TestCases von unittest erbt '''
class Test_data_processing(unittest.TestCase):
    
  # Test mit nicht existenter DB
  def test_db_nicht_existent_read_data(self):
      with self.assertRaises(FileNotFoundError):
        data_processing.read_data(falsche_database,falsche_tabelle,*falsche_spalten)
        
        
  # Test mit nicht leerer Datenbanktabelle DB
  def test_tabelle_ohne_Daten_read_data(self):
      with self.assertRaises(KeyError):
        data_processing.read_data(test_database,'testdaten','x','y')
 
# Skript im unittest-Kontext ausführen
if __name__ == '__main__':
  unittest.main()
 