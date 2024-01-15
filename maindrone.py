import sys
from PyQt5.QtWidgets import  QApplication,QApplication
import modele
import math
import scenegraphique
import drone_monitoring
import fenetres



Modele=modele.Modele()


     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("c tout bon")
    scene = scenegraphique.MaSceneGraphique()
    
    # Crée la vue graphique directement
    #view = QGraphicsView(scene)
    #view.show()


    voliere = drone_monitoring.ClientVoliere()
    fenetre = fenetres.MaFenetrePrincipale()


    voliere.drone_data.connect(fenetre.update_drone_data)
    #if voliere.drone_data[0]==888:
    #    tojason.Drone.posit=(voliere.drone_data[1],voliere.drone_data[2],voliere.drone_data[3])

    app.aboutToQuit.connect(voliere.stop)

    
    sys.exit(app.exec_())
