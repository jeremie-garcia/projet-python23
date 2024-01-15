
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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
