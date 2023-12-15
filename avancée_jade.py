import sys
import typing
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QAction, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QIcon, QPolygon
from PyQt5.QtCore import Qt, QPointF, QPoint
import tojason

v1 = tojason.Drone('v1',[20,20,20],[300,300,20],0)
Modele=tojason.Modele()
ang_drone=0


class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)


class VehiculeItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule                        #je recupere les données du vehicule choisis
        self.x1= vehicule.posit[0]
        self.y1= vehicule.posit[1]
        self.x2= vehicule.posit[0] - 25
        self.y2= vehicule.posit[1] - 100
        self.x3= vehicule.posit[0] - 50
        self.y3=vehicule.posit[1]
        self.polygone = QPolygonF([                              #je fais un polygone triangle
                        QPointF(self.x1, self.y1),
                        QPointF(self.x2, self.y2 ),
                        QPointF(self.x3, self.y3)
                    ])
        
        super(QGraphicsPolygonItem,self).__init__(self.polygone)

        self.newx=0
        self.newy=0
        
        self.setRotation(self.drone.orient)
        self.setBrush(QBrush(Qt.cyan))
        self.setPen(QPen(Qt.blue))

        Modele.add_drone(self.drone)


    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        print("press", event)
    
    def mouseMoveEvent(self, event):
        #quand on bouge alors on change la position du drone
        # print("move",event.scenePos())
        self.newx=event.scenePos().x()                                #je recupere la position de la souris
        self.newy=event.scenePos().y()
        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
        self.update_position()
        
    def update_position(self):
        self.setRotation(self.drone.orient)
        self.drone.posit[0]=self.newx                           #je change la position du drone
        self.drone.posit[1]=self.newy

        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        print(self.newx)
        print(self.newy)
        print(self.drone.posit)


# class Q_graphical_item(cm.Drone,cm.Building):

#     def __init__(self,Lbuild,Lvehic):
#         self.Lbuild = Lbuild
#         self.Lvehic = Lvehic

  
#     def dessinerCarre(self):
#         # Dessiner juste un carré sur la scène
#         carre_item = self.scene.addRect(0, 0, 50, 50)
#         carre_item.setPos(50, 50)
#         carre_item.setBrush(QBrush(Qt.red))
#         carre_item.setPen(QPen(Qt.black))
        

#     def ajouterTriangle(self):
#         # Ajouter un triangle à la scène
#         # Utiliser QPolygonF avec QPointF pour définir les points du triangle
#         for v in self.Lvehic:
#             triangle_item = self.scene.addPolygon(QPolygonF([QPointF(cm.v[0].posit[0],cm.v[0].posit[1]), QPointF(cm.v[1].posit[0],cm.v[1].posit[1]), QPointF(cm.v[2].posit[0],cm.v[2].posit[1])]))
#             triangle_item.setPos(150, 50)
#             triangle_item.setBrush(QBrush(Qt.cyan))
#             triangle_item.setPen(QPen(Qt.black))
        

#         # Définir l'angle de rotation pour le triangle (en degrés)
#         triangle_item.setRotation(ang_drone) # Vous pouvez ajuster l'angle selon vos besoins



class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.scene = MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.setCentralWidget(self.vue)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        toolbar=QToolBar("Paramètres")
        self.addToolBar(Qt.LeftToolBarArea,toolbar)
        toolbar.setMovable(False)
        bouton_ajouter_un_drone=QPushButton("Ajouter un drone")
        toolbar.addWidget(bouton_ajouter_un_drone)
        bouton_ajouter_un_drone.clicked.connect(self.ajoute_drone)
        bouton_ajouter_un_obstacle=QPushButton("Ajouter un obstacle")
        toolbar.addWidget(bouton_ajouter_un_obstacle)
        self.show()
        self.model = tojason.Modele()



    def ajoute_drone(self):
        #creer un drone
        drone = tojason.Drone("AC1", [0,0,0], [0,0,0], ang_drone)
        self.model.add_drone(drone)

        droneItem = VehiculeItem(drone)
        self.scene.addItem(droneItem)


def main():
    app = QApplication(sys.argv)
    print("c tout bon")
    fenetre = MaFenetrePrincipale()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



Lbuild=[]
Lvehic=[]
