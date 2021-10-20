'''
Programmmodul fuer die Hausarbeit zum Kurs  DLMDWPMP01 - Programmieren mit Python

Autor: Sebastian Kinnast Martikelnr.: 32112741

Tutor: Stephan Fuehrer
'''

import matplotlib.pyplot as plt
import pandas as np

def data_visualization(X,Y,a,b,titel):    
    ''' Zeichne x-,y-Werte und Regressionsgerade'''    
    max_x = np.max(X) #+ 100
    min_x = np.min(X) #- 100
    
    ''' Berechne x und y-Werte sowie Achsenabschnitte'''
    x_values = np.linspace(min_x, max_x, 10)
    y_values = a + b * x_values
     
    ''' Zeichne Gerade '''
    plt.plot(x_values, y_values, color='#58b970', label='Regressionsgerade')
    ''' Zeichne Scatter Points '''
    plt.scatter(X, Y, c='#ef5423', label=f'Scatter Plot')
     
    plt.title(titel)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()