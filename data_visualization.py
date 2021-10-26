'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

import matplotlib.pyplot as plt
import numpy as np
import random

def create_scatter_plot1(X,Y,label,titel):    
 
   ''' Zeichne Punkte-Wolke '''
   plt.scatter(
           X
           ,Y
           ,c=["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
           ,label = label
           )
   
   
   plt.title(titel)
   plt.xlabel('x')
   plt.ylabel('y')
   plt.legend()
   plt.show()

def create_scatter_plot2(*daten,titel):    
 
   ''' Zeichne Punkte-Wolke '''
   for tabelle in daten:
       plt.scatter(
               daten['x']
               ,daten['y']
               ,c=["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
               ,label = daten['label'].groupby(daten['label'])
               )
   
   
   plt.title(titel)
   plt.xlabel('x')
   plt.ylabel('y')
   plt.legend()
   plt.show()