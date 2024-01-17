import sys
from PyQt5.QtWidgets import  QApplication,QApplication
import modele
import scenegraphique
import drone_monitoring
import fenetres

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("lancement du programme")
    scene = scenegraphique.MaSceneGraphique()

    voliere = drone_monitoring.ClientVoliere()
    fenetre = fenetres.MaFenetrePrincipale()

    voliere.drone_data.connect(fenetre.update_drone_data)

    app.aboutToQuit.connect(voliere.stop)

    
    sys.exit(app.exec_())
