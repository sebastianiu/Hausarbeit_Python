'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

''' Benutzedefinierte Exceptions '''

''' Exception für den Fall, dass die abgefragte Datenbank-Datei nicht existiert '''
class databasefilenotfound(FileNotFoundError):
      # Konstruktor definieren
      def __init__(self):
      
          # eine eigene Nachricht als Attribut definieren 
          error_message = 'Datenbank-Datei im vorgegebenen Verzeichnis nicht gefunden.'
          self.error_message = error_message
    
    
    
