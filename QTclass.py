import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QPushButton, QToolBar, QAction, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QIcon
from PyQt5.QtCore import Qt, QPointF
import classmodel as cm

v1 = cm.Drone('v1',[20,20,20],[300,300,20],0)
ang_drone=0

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)



class vehicleItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule
        self.polygone = QPolygonF(QPointF(vehicule.posit[0],vehicule.posit[1]), QPointF(vehicule.posit[0] - 1,vehicule.posit[1] - 1), QPointF(vehicule.posit[0] - 1,vehicule.posit[1] + 1))
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
        self.setRotation(self.drone.orientation[1])

        self.setBrush(QBrush(Qt.cyan))
        self.setPen(QPen(Qt.black))

        def mouseMoveEvent(evt):
            #quand on bouge alors on change la position du drone
            self.drone.set_position(evt.posInScene().x(), evt.posInScene().y())
            self.update_position()
        
        def update_position(self):
             self.setRotation(self.drone.orientation[1])
             self.setPos(self.drone.position())





class Q_graphical_item(cm.Drone,cm.Building):

    def __init__(self,Lbuild,Lvehic):
        self.Lbuild = Lbuild
        self.Lvehic = Lvehic

  
    def dessinerCarre(self):
        # Dessiner juste un carré sur la scène
        carre_item = self.scene.addRect(0, 0, 50, 50)
        carre_item.setPos(50, 50)
        carre_item.setBrush(QBrush(Qt.red))
        carre_item.setPen(QPen(Qt.black))
        

    def ajouterTriangle(self):
        # Ajouter un triangle à la scène
        # Utiliser QPolygonF avec QPointF pour définir les points du triangle
        for v in self.Lvehic:
            triangle_item = self.scene.addPolygon(QPolygonF([QPointF(cm.v[0].posit[0],cm.v[0].posit[1]), QPointF(cm.v[1].posit[0],cm.v[1].posit[1]), QPointF(cm.v[2].posit[0],cm.v[2].posit[1])]))
            triangle_item.setPos(150, 50)
            triangle_item.setBrush(QBrush(Qt.cyan))
            triangle_item.setPen(QPen(Qt.black))
        

        # Définir l'angle de rotation pour le triangle (en degrés)
        triangle_item.setRotation(ang_drone) # Vous pouvez ajuster l'angle selon vos besoins



class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.scene = MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.setCentralWidget(self.vue)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.show()

        self.model = cm.Modele()

        bouton_ajouter_drone = QPushButton("Ajouter un drone")
        bouton_ajouter_drone.clicked.connect(self.ajoute_drone)

    def ajoute_drone(self):
        #creer un drone
        drone = cm.Drone("AC1", [0,0,0], [0,0,0], ang_drone)
        self.model.add_drone(drone)

        #object graohique qui represente le véhicule
        droneItem = vehicleItem(drone)
        self.scene.addItem(droneItem)


def main():
    app = QApplication(sys.argv)
    fenetre = MaFenetrePrincipale()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



Lbuild=[]
Lvehic=[]
