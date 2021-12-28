'''
Programmmodul für Benutzerdefinierte Exceptions

zur Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

''' Benutzerdefinierte Exceptions '''
        
class DatabaseTableEmptyError(LookupError):
    ''' Exception wenn abgefragte Datenbank-Tabelle keine Daten enthält '''
    # Konstruktor definieren
    def __init__(self,table):
        # eine eigene Nachricht als Attribut definieren 
        error_message = f"""Exception: Datenbank-Tabelle "{table}" enthält keine Daten.
        """
        self.error_message = error_message
        
class DatabaseTableAlreadyFullError(LookupError):
    ''' Exception wenn Tabelle als Importziel bereits Daten enthält '''
    # Konstruktor definieren
    def __init__(self,table):
        # eine eigene Nachricht als Attribut definieren 
        error_message = f"""Exception: Datenbank-Tabelle "{table}" existiert bereits und enthält Daten.'        
        """
        self.error_message = error_message 
        
class DatabaseTableNotExistsError(LookupError):
    ''' Exception wenn Tabelle nicht existiert'''
    # Konstruktor definieren
    def __init__(self,table):
        # eine eigene Nachricht als Attribut definieren 
        error_message = f"""Exception: Datenbank-Tabelle "{table}" existiert nicht.
        """
        self.error_message = error_message        
        
class DataFrameEmptyError(LookupError):
    ''' Exception wenn abgefragtes DataFrame keine Daten enthält '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = """Exception: DataFrame enthält keine Daten.
        """
        self.error_message = error_message

class ListEmptyError(LookupError):
    ''' Exception wenn abgefragte Liste keine Daten enthält '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = """Exception: Liste enthält keine Daten.
        """
        self.error_message = error_message         
        
class WrongFileFormatError(KeyError):
    ''' Exception, wenn falsches Dateiformat an funktion übergeben wird '''
    # Konstruktor definieren
    def __init__(self):
        # eine eigene Nachricht als Attribut definieren 
        error_message = """Exception: Falsche Datei-Format, nur CSV erlaubt.
        """
        self.error_message = error_message