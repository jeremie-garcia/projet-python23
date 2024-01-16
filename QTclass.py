import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar,QGraphicsItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF,QRectF
import tojason
from drone_monitoring import ClientVoliere
import math

Modele=tojason.Modele()

ang_drone=0
ang_goal=0
source_strength=0.5
imag_source_strength=0.5
sink_strength=5
safety=0.0001


class GridItem(QGraphicsItem):
    def __init__(self, rect, horizontalSpacing, verticalSpacing):
        super(GridItem, self).__init__()

        self.rect = rect
        self.horizontalSpacing = horizontalSpacing
        self.verticalSpacing = verticalSpacing

    def paint(self, painter, option, widget): #option, widget il faut les laisser
        pen = QPen()
        pen.setColor(Qt.lightGray)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        # lignes horizontales
        current_y = int(self.rect.top())
        while current_y <= int(self.rect.bottom()):
            painter.drawLine(int(self.rect.left()), current_y, int(self.rect.right()), current_y)
            current_y += self.verticalSpacing

        # lignes verticales
        current_x = int(self.rect.left())
        while current_x <= int(self.rect.right()):
            painter.drawLine(current_x, int(self.rect.top()), current_x, int(self.rect.bottom()))
            current_x += self.horizontalSpacing

    def boundingRect(self):
        return QRectF(self.rect)



class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)

        rect_item = QGraphicsRectItem(-400, -400, 800, 800)
        self.addItem(rect_item)

        grid_item = GridItem(rect_item.boundingRect(), 50, 50)  # Ajustez les valeurs entres les lignes
        self.addItem(grid_item)





class ObstacleItem(QGraphicsPolygonItem):
    def __init__(self,building):

        self.building = building
        self.polygonpoints=[]
        #pour chaque vertices (x,y,z) je cree un point QTpointf et j'ajoute dans la liste
        for vertice in building.vertices:
            self.polygonpoints.append(QPointF(vertice[0],vertice[1]))
            

        self.polygone = self.polygone = QPolygonF( self.polygonpoints )
        
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
        
        #self.setRotation(self.drone.orient)
        self.setBrush(QBrush(Qt.red))
        self.setPen(QPen(Qt.red))
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
        nbs_sommets=len(self.building.vertices)
        for i in range (nbs_sommets):
            angle = 2 * math.pi * i / nbs_sommets
            self.building.vertices[i][0]=self.newx + 60 * math.cos(angle)
            self.building.vertices[i][1]=self.newy + 60 * math.sin(angle)
        

        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le building dans l'interface
        #print(self.building.vertices)






class VehiculeItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule
        self.x1= vehicule.position[0]
        self.y1= vehicule.position[1]
        self.x2= vehicule.position[0] - 25
        self.y2= vehicule.position[1] - 50
        self.x3= vehicule.position[0] - 50
        self.y3=vehicule.position[1]
        self.polygone = QPolygonF([                              #je fais un polygone triangle
                        QPointF(self.x1, self.y1),
                        QPointF(self.x2, self.y2 ),
                        QPointF(self.x3, self.y3)
                    ])
        
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
        
        self.setRotation(self.drone.orientation)
        self.setBrush(QBrush(Qt.cyan))
        self.setPen(QPen(Qt.cyan))
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
        self.setRotation(self.drone.orientation)
        self.drone.position[0]=self.newx
        self.drone.position[1]=self.newy
        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        #print(self.drone.target)

    



class GoalItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule
        self.x1= vehicule.goal[0]
        self.y1= vehicule.goal[1]
        self.x2= vehicule.goal[0] - 25
        self.y2= vehicule.goal[1] - 50
        self.x3= vehicule.goal[0] - 50
        self.y3=vehicule.goal[1]
        self.polygone = QPolygonF([                              #je fais un polygone triangle
                        QPointF(self.x1, self.y1),
                        QPointF(self.x2, self.y2 ),
                        QPointF(self.x3, self.y3)
                    ])
        
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
        
        self.setRotation(self.drone.orientation)
        self.setBrush(QBrush(Qt.green))
        self.setPen(QPen(Qt.green))

        
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        print("press", event)
    
    def mouseMoveEvent(self, event):
        #quand on bouge alors on change la position du drone
        # print("move",event.scenePos())
        self.newx=event.scenePos().x()                                #je recupere la position de la souris
        self.newy=event.scenePos().y()

        self.drone.goal[0]=self.newx                           #je change la position du building
        self.drone.goal[1]=self.newy

        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
        self.update_position()
        
    def update_position(self):
        self.setRotation(self.drone.orientation)

        self.setPos(QPointF(self.newx, self.newy))                  
        #print(self.drone.goal)



class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.scene = MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.vue.fitInView(self.scene.itemsBoundingRect(),Qt.KeepAspectRatio)
        self.setCentralWidget(self.vue)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        toolbar=QToolBar("Paramètres")
        self.addToolBar(Qt.LeftToolBarArea,toolbar)
        toolbar.setMovable(False)


        bouton_ajouter_un_drone=QPushButton("Ajouter un drone")
        toolbar.addWidget(bouton_ajouter_un_drone)
        bouton_ajouter_un_drone.clicked.connect(self.ajoute_drone)

        bouton_ajouter_un_buildingcarre=QPushButton("Ajouter un obstacle carrée")
        toolbar.addWidget(bouton_ajouter_un_buildingcarre)
        bouton_ajouter_un_buildingcarre.clicked.connect(self.ajoute_buildingcarre)

        bouton_ajouter_un_buildinghexa=QPushButton("Ajouter un obstacle hexagonale")
        toolbar.addWidget(bouton_ajouter_un_buildinghexa)
        bouton_ajouter_un_buildinghexa.clicked.connect(self.ajoute_buildinghexa)

        bouton_creerjason = QPushButton("creer le jason")
        toolbar.addWidget(bouton_creerjason)
        bouton_creerjason.clicked.connect(self.creer_json)
        
        self.show()

        self.model = tojason.Modele()

    def creer_json(self):
        modele = Modele
        modele.json('fichier jason')

        



    def update_drone_data(self, AC_ID, pos_x, pos_y,pos_z, quat_a, quat_b, quat_c, quat_d):
        if(AC_ID == 68):
           self.model.drone[0].position=(pos_x,pos_y,pos_z) 
           print(AC_ID, pos_x, pos_y)



    def ajoute_drone(self):
        #creer un drone
        drone = tojason.Drone("68", [0,0,0],[0,0,0], ang_drone, source_strength, imag_source_strength, sink_strength, safety)
        self.model.add_drone(drone)

        droneItem = VehiculeItem(drone)
        goalItem = GoalItem(drone)
        self.scene.addItem(droneItem)
        self.scene.addItem(goalItem)
    

    
    def ajoute_buildingcarre(self):
        vertices=[[0,0,151.5],[0,60.5,151.5],[60.50,60.5,151.5],[60.5,0,151.5]]
        building = tojason.Building("OBScarré",vertices)
        self.model.add_building(building)

        buildingItem = ObstacleItem(building)
        self.scene.addItem(buildingItem)


    def ajoute_buildinghexa(self):
        vertices=[[60,0,151.5],[30,51.96,151.5],[-30,51.96,151.5],[-60,0,151.5],[-30,-51.96,151.5],[30,-51.96,151.5]]
        building = tojason.Building("OBShexa",vertices)
        self.model.add_building(building)

        buildingItem = ObstacleItem(building)
        self.scene.addItem(buildingItem)

     

def main():
    app = QApplication(sys.argv)
    print("c tout bon")

    voliere = ClientVoliere()
    fenetre = MaFenetrePrincipale()


    voliere.drone_data.connect(fenetre.update_drone_data)
    #if voliere.drone_data[0]==888:
    #    tojason.Drone.posit=(voliere.drone_data[1],voliere.drone_data[2],voliere.drone_data[3])

    app.aboutToQuit.connect(voliere.stop)

    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



Lbuild=[]
Lvehic=[]
