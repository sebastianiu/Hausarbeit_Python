"""
Programm fÃ¼r die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan FÃ¼hrer
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.orm import declarative_base

def Datenbank_erzeugen(Datenbankname):
    """Engine-Objekt erzeugen """
    engine = create_engine(f"sqlite+pysqlite:///{Datenbankname}.db",future = True, echo = True)
    
    """Base-Objekt als Baisis für Tabellenklassene rzeugen """
    Base = declarative_base()
    
    """Tabellenklasse deklarieren"""
    class testdaten(Base):
        __tablename__ = 'testdaten'        
        x = Column(Integer,primary_key=True)
        y1 = Column(Integer)              
        
        '''
        __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'testdaten'
        }
        #re_trainingsdaten = relationship("trainingsdaten", back_populates="testdaten")
        '''
    class trainingsdaten(Base):
        __tablename__ = 'trainingsdaten'
        
        x = Column(Integer,primary_key=True)
        y1 = Column(Integer)
        y2 = Column(Integer)
        y3 = Column(Integer)
        y4 = Column(Integer)  
               
    class ergebnisdaten(Base):
        __tablename__ = 'ergebnisdaten'
        
        x = Column(Integer,primary_key=True)
        y1 = Column(Integer)
        y2 = Column(Integer)
        delta_y = Column(Integer)
        funk_nr = Column(Integer)
      
    class ideale_funktionen(Base):
        __tablename__ = 'ideale_funktionen'
        
        x = Column(Integer,primary_key=True)
        y1 = Column(Integer)
        y2 = Column(Integer)
        y3 = Column(Integer)
        y4 = Column(Integer)
        y5 = Column(Integer)
        y6 = Column(Integer)
        y7 = Column(Integer)
        y8 = Column(Integer)
        y9 = Column(Integer)
        y10 = Column(Integer)
        y11 = Column(Integer)
        y12 = Column(Integer)
        y13 = Column(Integer)
        y14 = Column(Integer)
        y15 = Column(Integer)
        y16 = Column(Integer)
        y17 = Column(Integer)
        y18 = Column(Integer)
        y19 = Column(Integer)
        y20 = Column(Integer)
        y21 = Column(Integer)
        y22 = Column(Integer)
        y23 = Column(Integer)
        y24 = Column(Integer)
        y25 = Column(Integer)
        y26 = Column(Integer)
        y27 = Column(Integer)
        y28 = Column(Integer)
        y29 = Column(Integer)
        y30 = Column(Integer)
        y31 = Column(Integer)
        y32 = Column(Integer)
        y33 = Column(Integer)
        y34 = Column(Integer)
        y35 = Column(Integer)
        y36 = Column(Integer)
        y37 = Column(Integer)
        y38 = Column(Integer)
        y39 = Column(Integer)
        y40 = Column(Integer)
        y41 = Column(Integer)
        y42 = Column(Integer)
        y43 = Column(Integer)
        y44 = Column(Integer)
        y45 = Column(Integer)
        y46 = Column(Integer)
        y47 = Column(Integer)
        y48 = Column(Integer)
        y49 = Column(Integer)
        y50 = Column(Integer)  
     
    """Alle Metadaten-Objekte erzeugen """
    Base.metadata.create_all(engine)    
        
Datenbank_erzeugen("Testdatenbank")




'''
engine = create_engine("sqlite+pysqlite:///:memory:",future = True, echo = True)#test_sqlite_db.db',future = True, echo = True)

with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10},{"x" : 1 ,"y" : 1},{"x" : 2, "y" :4}]
        )
    
    result = conn.execute(text('Select x, y from some_table'))
    for row in result:
        print(row)
    #conn.commit()
'''

         
''' 
     Ergänze Attribute y2 bis y50 
     for i in range(2,51):
        setattr(ideale_funktionen,f'y{i}','integer')  
'''         




