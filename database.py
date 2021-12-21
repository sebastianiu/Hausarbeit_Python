'''
Programmmodul für die Datenmodell-Erstellung

zur die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Matrikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
from sqlalchemy import create_engine, MetaData, Table, Column, Float,String
from sqlalchemy.orm import declarative_base,relationship
import os,sys
import user_exceptions as ue


class Database:
    '''Funktion um eine SQLite-Datenbank/ -Veribdunung ,mittels Engine-Objekt zu erzeugen'''
    def __init__(self):
        self.connection = create_engine('sqlite:///Programmdatenbank.db', echo=False)   
       
class data_processing(Database):
    
    def import_data(self,data,table,):    
        
        ''' Funktion zum Auslesen von Daten aus einer CSV-Datei und import in eine 
        SQLLite-DB-Tabelle 
        ''' 
        data.to_sql(table,con=self.connection,if_exists='fail',index = False,
                                                index_label = 'recordid'
                                                )        
       
        
'''
    def create_database(self):
      #Funktion zur Erstellung der SQLite-Datenbank-Datei und den erfoderlichen 
       # Tabellen
       
        try:
            # Prüfen ob zu erstellende Datei bereits existiert
            if os.path.exists(f'Datenbank\{self.Datenbankname}.db') == False:              
                # Engine-Objekt erzeugen
                engine = create_engine(f'sqlite:///Datenbank\{self.Datenbankname}.db',future = True,
                                       echo = True)               
                
                
                
                Base = declarative_base()
                               
                
                #Tabellen-Klassen definieren
                class Testdaten(Base):
                    __tablename__ = 'Testdaten'            
                    x = Column(Float,primary_key=True)
                    y = Column(Float,primary_key=True)
                    delta_y = Column(Float)
                    funkt_nr = Column(String)   
                  
                class Trainingsdaten(Base):
                    __tablename__ = 'Trainingsdaten'             
                    x = Column(Float,primary_key=True)            
                    y1 = Column(Float)
                    y2 = Column(Float)
                    y3 = Column(Float)
                    y4 = Column(Float)       
                
                class Ideale_Funktionen(Base):
                    __tablename__ = 'Ideale_Funktionen'           
                    x = Column(Float,primary_key=True)
                    y1 = Column(Float)
                    y2 = Column(Float)
                    y3 = Column(Float)
                    y4 = Column(Float)
                    y5 = Column(Float)
                    y6 = Column(Float)
                    y7 = Column(Float)
                    y8 = Column(Float)
                    y9 = Column(Float)
                    y10 = Column(Float)
                    y11 = Column(Float)
                    y12 = Column(Float)
                    y13 = Column(Float)
                    y14 = Column(Float)
                    y15 = Column(Float)
                    y16 = Column(Float)
                    y17 = Column(Float)
                    y18 = Column(Float)
                    y19 = Column(Float)
                    y20 = Column(Float)
                    y21 = Column(Float)
                    y22 = Column(Float)
                    y23 = Column(Float)
                    y24 = Column(Float)
                    y25 = Column(Float)
                    y26 = Column(Float)
                    y27 = Column(Float)
                    y28 = Column(Float)
                    y29 = Column(Float)
                    y30 = Column(Float)
                    y31 = Column(Float)
                    y32 = Column(Float)
                    y33 = Column(Float)
                    y34 = Column(Float)
                    y35 = Column(Float)
                    y36 = Column(Float)
                    y37 = Column(Float)
                    y38 = Column(Float)
                    y39 = Column(Float)
                    y40 = Column(Float)
                    y41 = Column(Float)
                    y42 = Column(Float)
                    y43 = Column(Float)
                    y44 = Column(Float)
                    y45 = Column(Float)
                    y46 = Column(Float)
                    y47 = Column(Float)
                    y48 = Column(Float)
                    y49 = Column(Float)
                    y50 = Column(Float)  
                    
                #Alle Metadaten-Objekte (Tabellen) erzeugen
                Base.metadata.create_all(engine)                  
                print(f'\nNeue Datenbank-Datei {self.Datenbankname} erzeugt und ' 
                      'Tabellen generiert.\n')  
                                              
            else:
                raise DatabaseFileAlreadyExists           
                
        except DatabaseFileAlreadyExists:
             print(DatabaseFileAlreadyExists().error_message)
        
'''   
