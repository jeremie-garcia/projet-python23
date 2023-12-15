import sys
import typing
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QAction, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QIcon, QPolygon
from PyQt5.QtCore import Qt, QPointF, QPoint
import tojason as cm
import tojason

v1 = tojason.Drone('v1',[20,20,20],[300,300,20],0)
Modele=tojason.Modele()
ang_drone=0

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)

        self.addItem(QGraphicsRectItem(-50,-50, 100, 100))




class ObstacleItem(QGraphicsPolygonItem):
    def __init__(self,building):

        self.building = building
        self.polygonpoints=[]
        #pour chaque vertices (x,y,z) je cree un point QTpointf et j'ajoute dans la liste
        for vertice in building.verticies:
            self.polygonpoints.append(QPointF(vertice[0],vertice[1]))
            

        self.polygone = self.polygone = QPolygonF( self.polygonpoints )
        
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
        
        #self.setRotation(self.drone.orient)
        self.setBrush(QBrush(Qt.cyan))
        self.setPen(QPen(Qt.cyan))
        Modele.add_building(self.building)

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
        #self.setRotation(self.drone.orient)
        self.building.verticies[0]=self.newx                           #je change la position du drone
        self.building.verticies[1]=self.newy

        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        print(self.newx)
        print(self.newy)
        print(self.building.verticies)






class VehiculeItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule
        self.x1= vehicule.posit[0]
        self.y1= vehicule.posit[1]
        self.x2= vehicule.posit[0] - 2.5
        self.y2= vehicule.posit[1] - 10
        self.x3= vehicule.posit[0] - 5
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
        self.setBrush(QBrush(Qt.red))
        self.setPen(QPen(Qt.red))

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
        self.drone.posit[0]=self.newx                           #je change la position du building
        self.drone.posit[1]=self.newy

        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        print(self.newx)
        print(self.newy)
        print(self.drone.posit)

    




class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.scene = MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.vue.fitInView(self.scene.itemsBoundingRect())
        self.setCentralWidget(self.vue)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        toolbar=QToolBar("Paramètres")
        self.addToolBar(Qt.LeftToolBarArea,toolbar)
        toolbar.setMovable(False)


        bouton_ajouter_un_drone=QPushButton("Ajouter un drone")
        toolbar.addWidget(bouton_ajouter_un_drone)
        bouton_ajouter_un_drone.clicked.connect(self.ajoute_drone)

        bouton_ajouter_un_building=QPushButton("Ajouter un obstacle")
        toolbar.addWidget(bouton_ajouter_un_building)
        bouton_ajouter_un_building.clicked.connect(self.ajoute_building)
        
        self.show()

        self.model = tojason.Modele()

        

    def ajoute_drone(self):
        #creer un drone
        drone = cm.Drone("AC1", [0,0,0,],[0,0,0], ang_drone)
        self.model.add_drone(drone)

        droneItem = VehiculeItem(drone)
        self.scene.addItem(droneItem)

    
    def ajoute_building(self):
        verticies=[[0,0,1],[0,10,1],[10,10,1],[10,0,1]]
        building = cm.Building("OBS1",verticies)
        self.model.add_building(building)

        buildingItem = ObstacleItem(building)
        self.scene.addItem(buildingItem)
    
     
        
    


def main():
    app = QApplication(sys.argv)
    print("c tout bon")
    fenetre = MaFenetrePrincipale()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



Lbuild=[]
Lvehic=[]
