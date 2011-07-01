from matplotlib import pyplot,lines 
from pylab import *
import numpy
class Dibujar():
    t = "Itempetei"
    N = 4
    
    nombreFases = ['fase1','fase2','fase3','fase4']
    matriz = numpy.zeros((5,5))
    x = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4]
    y = [1,2,3,4,1,2,3,4,1,2,3,4,1,3,4]
    clf()
    
    a,b = numpy.array([[2, 3, 4], [1,2, 3]])
    c,d = numpy.array([[2,2], [1,2]])
    
    ind = np.arange(N)
    width = 1 
    #ax2 = pyplot.axes()
    
    
    
    plt.text(1, 1, t, family='Item 1', style='italic', ha='center')
    plt.text(1, 2, 'nombreItem', family='Item 1', style='italic', ha='center')
    #b,g,k(negro),m, 1(blanco)
    plt.annotate('', xy=(2, 2), xytext=(2, 1),arrowprops=dict(facecolor='1', shrink=0.03),)
    plt.annotate('', xy=(2, 1), xytext=(1, 4),arrowprops=dict(facecolor='b', shrink=0.03),)
    plt.annotate('', xy=(3, 3), xytext=(2, 1),arrowprops=dict(facecolor='b', shrink=0.03),)
    ## xy es donde termina la flecha... xytext es donde empiesa la flecha
    plot(x, y, 'H', markeredgecolor='#90D0E1', markeredgewidth=1, markerfacecolor='#90D0E1', markersize=40)
    
    
    axis([0, 5, 0, 5])
    plt.title('Fases del Proyecto')
    #for fase in nombreFases:
    plt.xticks(ind+width, nombreFases )
    pyplot.savefig( 'ojala.png' )
    plt.show()
