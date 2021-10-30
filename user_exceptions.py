'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

''' Benutzerdefinierte Exceptions '''

class DatabaseFileNotFoundError(FileNotFoundError):
    ''' Exception, wenn abgefragte Datenbank-Datei nicht existiert '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = 'Datenbank-Datei wurde im vorgegebenen Verzeichnis \
nicht gefunden.'
        self.error_message = error_message    
        
class DatabaseFileAlreadyExists(OSError):
    ''' Exception, wenn zu erzeugende Datenbank-Datei bereits existiert '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = 'Datenbank-Datei existiert im vorgegebenen Verzeichnis \
bereits.'
        self.error_message = error_message
        
class DatabaseTableEmptyError(LookupError):
    ''' Exception wenn abgefragte Datenbank-Tabelle keine Daten enthält '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = 'Datenbank-Tabelle enthält keine Daten.'
        self.error_message = error_message
        
        
        
    
    
    
    
