import sys
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QSpacerItem, QSizePolicy, QComboBox, QDialog, QGraphicsView,QVBoxLayout,QHBoxLayout,QLabel, QLineEdit,QWidget, QSlider, QApplication,QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar,QGraphicsItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen,QPixmap,QTransform, QPainter, QIcon 
from PyQt5.QtCore import Qt, QPointF, QSize
import tojason
#from drone_monitoring import ClientVoliere
import math
#from gflow.utils.plot_utils import PlotTrajectories
#from gflow.cases import Cases
#from gflow.utils.simulation_utils import run_simulation



Modele=tojason.Modele()

ang_drone=180
ang_goal=180


class ImageGridItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None):
        super(ImageGridItem, self).__init__(pixmap, parent)

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)

        # Définir la taille de l'image (carrée)
        image_size = 800

        # Charger l'image et redimensionner
        image_path = 'grilleflipped.jpg'

        

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





class GoalItem(QGraphicsPolygonItem):
    def __init__(self,vehicule):

        self.drone = vehicule
        self.x1= vehicule.position[0] + 25
        self.y1= vehicule.position[1] + 25
        self.x2= vehicule.position[0] 
        self.y2= vehicule.position[1] - 25
        self.x3= vehicule.position[0] - 25
        self.y3=vehicule.position[1] + 25
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










     
if __name__ == '__main__':
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