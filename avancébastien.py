import sys
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QComboBox, QDialog, QGraphicsView,QVBoxLayout,QHBoxLayout,QLabel, QLineEdit,QWidget, QSlider,QGraphicsRectItem, QApplication,QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar,QGraphicsItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen,QFont,QPixmap,QTransform, QPainter, QIcon 
from PyQt5.QtCore import Qt, QPointF,QRectF, QSize
import classmodel_tojson as tojason
from drone_monitoring import ClientVoliere
import math
#from PIL import Image


Modele=tojason.Modele()

ang_drone=180
ang_goal=180
source_strength=0.5
imag_source_strength=0.5
sink_strength=5
safety=0.0001



class ImageGridItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None):
        super(ImageGridItem, self).__init__(pixmap, parent)

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)

        # Définir la taille de l'image (carrée)
        image_size = 800

        # Charger l'image et redimensionner
        image_path = 'grille.png'

        

        #img = Image.open(image_path)
        #flipped_image = img.transpose(Image.FLIP_TOP_BOTTOM)
        #flipped_image.save('flipped_grille.png')

        #image_path = 'flipped_grille'

        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(image_size, image_size, Qt.KeepAspectRatio)

        

        # flippedimage = pixmap.toImage().mirrored(False,True)
        # flippedpixmap = QPixmap.fromImage(flippedimage)
        # imageItem = QGraphicsPixmapItem(flippedpixmap)

        # Calculer les coordonnées pour centrer l'image
        x_center = -image_size / 2
        y_center = -image_size / 2
        
        # Ajouter l'image à la scène
        grid_item = QGraphicsPixmapItem(scaled_pixmap)
        grid_item.setPos(x_center, y_center)
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
        if nbs_sommets == 4: # calcul des coordonées en fonctions de carré ou hexa
            self.building.vertices[0][0]= self.newx
            self.building.vertices[0][1]= self.newy 
            self.building.vertices[1][0]= self.newx
            self.building.vertices[1][1]= self.newy +60 
            self.building.vertices[2][0]= self.newx + 60 
            self.building.vertices[2][1]= self.newy +60 
            self.building.vertices[3][0]= self.newx + 60 
            self.building.vertices[3][1]= self.newy  
        else:

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
        self.setBrush(QBrush(Qt.black))
        self.setPen(QPen(Qt.cyan))
        Modele.add_drone(self.drone)




    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.RightButton:
            # Open the secondary window with drone details
            details_dialog = DroneDetailsDialog(self)
            details_dialog.exec_()
        elif event.button() == Qt.LeftButton:
            self.newx=event.scenePos().x()                                #je recupere la position de la souris
            self.newy=event.scenePos().y()
            print("press", event)
    
    # def mouseMoveEvent(self, event):
    #     #quand on bouge alors on change la position du drone
    #     # print("move",event.scenePos())
    #     self.newx=event.scenePos().x()                                #je recupere la position de la souris
    #     self.newy=event.scenePos().y()

    # def mouseRightclickEvent(self, eventR: QGraphicsSceneMouseEvent) -> None:
    #     if eventR.button() == Qt.RightButton:
    #         # Open the secondary window with drone details
    #         details_dialog = DroneDetailsDialog(self.drone.ID)
    #         details_dialog.exec_()

        

        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
        self.update_position()
        
    def update_position(self):
        self.setRotation(self.drone.orientation)
        self.drone.position[0]=self.newx
        self.drone.position[1]=self.newy
        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        #print(self.drone.target)

    def update_drone_color(self):
        color_name = DroneDetailsDialog.color_combobox.currentText()
        color_dict = {'Red': Qt.red, 'Green': Qt.green, 'Blue': Qt.blue, 'Yellow': Qt.yellow, 'Purple': Qt.magenta}
        self.setBrush(QBrush(color_dict.get(color_name, Qt.red)))




class DroneDetailsDialog(QDialog):
    def __init__(self, VehiculeItem):
        super(DroneDetailsDialog, self).__init__()

        self.setWindowTitle("Drone Details")
        self.setGeometry(100, 100, 300, 150)

        # Create QLabel to display drone name and color
        name_label = QLabel(f"Drone ID: {VehiculeItem.drone.ID}")
        

        self.color_combobox = QComboBox()
        self.color_combobox.addItems(['Red', 'Green', 'Blue', 'Yellow', 'Purple'])
        self.color_combobox.setCurrentIndex(0)
        self.color_combobox.currentIndexChanged.connect(VehiculeItem.update_drone_color)
       

        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

       # mets en place les layouts
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.color_combobox)
        
        layout.addWidget(ok_button)
        
        self.setLayout(layout)   
        self.show()

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
    






class ZoomButtonP(QPushButton):
    def __init__(self, icon_path, zoom_factor, *args, **kwargs):
        super(ZoomButtonP, self).__init__(*args, **kwargs)
        self.zoom_factor = zoom_factor
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(50, 50))  # Ajustez la taille de l'icône selon vos besoins
        self.clicked.connect(lambda: MaFenetrePrincipale.zoom(MaFenetrePrincipale,2))


        

class TriangleWidget(QPushButton):
    def __init__(self, main_window):
        super(TriangleWidget, self,).__init__()
        self.main_window = main_window  # Ajoutez une référence à la fenêtre principale
        self.clicked.connect(self.main_window.ajoute_drone)  # Connectez le clic à la méthode de la fenêtre principale
        self.setGeometry(0, 0, 100, 100)  # Ajustez la taille 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Définir les points du trig
        points = [QPointF(0, self.height()), QPointF(self.width(), self.height()), QPointF(self.width() / 2, 0)]

        # Créer le trig
        triangle_polygon = QPolygonF(points)

        # Dessiner le trig
        painter.setBrush(QBrush(Qt.cyan))
        painter.setPen(QPen(Qt.black))
        painter.drawPolygon(triangle_polygon)


class HexagonWidget(QPushButton):
    def __init__(self, main_window):
        super(HexagonWidget, self).__init__()
        self.main_window = main_window  
        self.clicked.connect(self.main_window.ajoute_buildinghexa)  
        self.setGeometry(0, 0, 50, 50)  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the points of the hexagon
        points = [
            QPointF(0, self.height()),
            QPointF(self.width() / 4, 0),
            QPointF(3 * self.width() / 4, 0),
            QPointF(self.width(), self.height()),
            QPointF(3 * self.width() / 4, 2 * self.height()),
            QPointF(self.width() / 4, 2 * self.height())
        ]

       
        hexagon_polygon = QPolygonF(points)

    
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.black))
        painter.drawPolygon(hexagon_polygon)


class CarreeWidget(QPushButton):
    def __init__(self, main_window):
        super(CarreeWidget, self).__init__()
        self.main_window = main_window  # Ajoutez une référence à la fenêtre principale
        self.clicked.connect(self.main_window.ajoute_buildingcarre)  # Connectez le clic à la méthode de la fenêtre principale
        self.setGeometry(0, 0, 50, 50)  # taille du widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Définir les points du carré
        points = [QPointF(0, 0), QPointF(self.width(), 0), QPointF(self.width(), self.height()), QPointF(0, self.height())]

        # On crée le carrée
        carree_polygon = QPolygonF(points)

       # on dessine
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.black))
        painter.drawPolygon(carree_polygon)


class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.scene = MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.vue.scale(1, -1)
        self.vue.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio) 
        self.button_jason = QPushButton('créer Jason')       
        # Créer un layout principal
        mainlayout = QHBoxLayout()

        # Ajouter layout1 à gauche
        layout1 = self.create_layout1()  # Vous devriez implémenter votre propre fonction pour créer layout1
        mainlayout.addLayout(layout1)

        # Ajouter la scène graphique à droite
        mainlayout.addWidget(self.vue)

        # Créer le widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainlayout)
        self.setCentralWidget(centralWidget)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.model = tojason.Modele()
        self.button_jason.clicked.connect(self.creer_json)


        self.show()

    def create_layout1(self):
        layout1 = QVBoxLayout()

        # Ajoutez des widgets à la mise en page
        # label_info = QLabel("Informations personnalisées")
        # layout1.addWidget(label_info)

       # Ajouter le triangle à votre layout personnalisé
        triangle_widget = TriangleWidget(self)
        layout1.addWidget(triangle_widget)



        # Ajouter le carree à notre layout 
        carree_widget = CarreeWidget(self)
        layout1.addWidget(carree_widget)

        # Ajouter l'hexagone a notre layout
        hexa_widget = HexagonWidget(self)
        layout1.addWidget(hexa_widget)

        #  # Ajouter des boutons de zoom à votre layout personnalisé
        zoom_in_button = ZoomButtonP('ZoomButtonP.png', 2.0, 'Zoom In')
        # zoom_out_button = ZoomButton('zoom_out_icon.png', 0.5, 'Zoom Out')
        layout1.addWidget(zoom_in_button)
        # layout1.addWidget(zoom_out_button)
    
        
        layout1.addWidget(self.button_jason)
        # self.button_jason.clicked.connect(self.creer_json)

        return layout1

    def zoom(self, facteur):
        echelle_actuelle = self.vue.transform().m11()
        nouvelle_echelle = echelle_actuelle * facteur
        self.vue.setTransform(QTransform().scale(nouvelle_echelle, nouvelle_echelle))


    def creer_json(self):
        modele = Modele
        modele.json('fichier jason')

        
    def update_drone_data(self, AC_ID, pos_x, pos_y,pos_z, quat_a, quat_b, quat_c, quat_d):
        # if(AC_ID == 68):
        #    self.model.drone[0].position=(pos_x,pos_y,pos_z) 
        #    print(AC_ID, pos_x, pos_y)

        for drone in Modele.drone:
            if drone.id == AC_ID:
                drone.position=(pos_x,pos_y,pos_z)



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
    scene = MaSceneGraphique()
    
    # Crée la vue graphique directement
    #view = QGraphicsView(scene)
    #view.show()


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

 
