'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''
from sqlalchemy import create_engine, MetaData, Table, Column, Float,ForeignKey,Integer,
String
from sqlalchemy.orm import declarative_base,relationship
import pandas as pd
import os,sys

def create_database_model(Datenbankname):
     # Existenz feststellen
     if os.path.exists(f'{Datenbankname}.db'):
         raise RuntimeError(f'Datenbankdatei "{Datenbankname}.db" ist bereits im Verzeichnis vorhanden.')
     else:       
        '''Engine-Objekt erzeugen'''
        engine = create_engine(f'sqlite:///{Datenbankname}.db',future = True,echo = True)     
        Base = declarative_base()
        
        class testdaten(Base):
            __tablename__ = 'testdaten'            
            x = Column(Float,primary_key=True)
            y = Column(Float,primary_key=True)
            delta_y = Column(Float)
            funkt_nr = Column(String)   
            
        class trainingsdaten(Base):
            __tablename__ = 'trainingsdaten'             
            x = Column(Float,primary_key=True)            
            y1 = Column(Float)
            y2 = Column(Float)
            y3 = Column(Float)
            y4 = Column(Float)       
     
        class ideale_funktionen(Base):
            __tablename__ = 'ideale_funktionen'           
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
    
        """ Alle Metadaten-Objekte erzeugen """
        Base.metadata.create_all(engine)      
              
        print(f'\nNeue Datenbank-Datei {Datenbankname} erzeugt und Tabellen generiert.\n')
    
   
    

    
