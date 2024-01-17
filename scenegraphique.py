from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)

        # Définir la taille de l'image (carrée)
        image_size = 800   #l'image est retournée à cause de l'inversion de l'axe y
        image_path = 'grilleflipped.jpg' #chemin d'accès de l'image   
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(image_size, image_size, Qt.KeepAspectRatio)
        
        # Calculer les coordonnées pour centrer l'image
        x_center = -image_size / 2
        y_center = -image_size / 2
        
        # Ajouter l'image à la scène
        grid_item = QGraphicsPixmapItem(scaled_pixmap)
        grid_item.setPos(x_center, y_center) # permet de bien positionner l'image
        self.addItem(grid_item)
