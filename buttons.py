from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtGui import QPolygonF, QBrush, QPen,QPixmap,QTransform, QPainter, QIcon 
from PyQt5.QtCore import Qt, QPointF, QSize
import math


class ZoomButtonP(QPushButton):
    def __init__(self, icon_path, zoom_factor, main_window , *args, **kwargs):
        super(ZoomButtonP, self).__init__(*args, **kwargs)
        self.zoom_factor = zoom_factor
        self.main_window = main_window
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(50, 50))  # Ajustez la taille de l'icône selon vos besoins
        # self.clicked.connect(lambda: MaFenetrePrincipale.zoom(MaFenetrePrincipale,2))

        self.clicked.connect(lambda : self.main_window.zoom(self.zoom_factor))


class ZoomButtonN(QPushButton):
    def __init__(self, icon_path2, zoom_factor, main_window , *args, **kwargs):
        super(ZoomButtonN, self).__init__(*args, **kwargs)
        self.zoom_factor = zoom_factor
        self.main_window = main_window
        self.setIcon(QIcon(icon_path2))
        self.setIconSize(QSize(50, 50))  # Ajustez la taille de l'icône selon vos besoins
        # self.clicked.connect(lambda: MaFenetrePrincipale.zoom(MaFenetrePrincipale,2))

        self.clicked.connect(lambda : self.main_window.zoom(self.zoom_factor))

        

class TriangleButton(QPushButton):
    def __init__(self, main_window):
        super(TriangleButton, self,).__init__()
        self.main_window = main_window  # Ajoutez une référence à la fenêtre principale
        self.clicked.connect(self.main_window.ajoute_drone)  # Connectez le clic à la méthode de la fenêtre principale
        self.setFixedSize(50, 50)  # Ajustez la taille 

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


class HexagonButton(QPushButton):
    def __init__(self, main_window):
        super(HexagonButton, self).__init__()
        self.main_window = main_window  
        self.clicked.connect(self.main_window.ajoute_buildinghexa)  
        self.setFixedSize(50, 50)  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)


        # Define the points of the regular hexagon
        side_length = self.width() / 2
        apothem = side_length * math.sqrt(3) / 2
        
        # Define the points of the hexagon
        points = [
            QPointF(self.width() / 4, 0),
            QPointF(3*self.width() / 4, 0),
            QPointF(self.width(), apothem),
            QPointF(3 * self.width() / 4, 2 * apothem),
            QPointF(self.width() / 4 , apothem * 2),
            QPointF(0, apothem)
        ]


       
        hexagon_polygon = QPolygonF(points)

        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.black))
        painter.drawPolygon(hexagon_polygon)


class SquareButton(QPushButton):
    def __init__(self, main_window):
        super(SquareButton, self).__init__()
        self.main_window = main_window  # Ajoutez une référence à la fenêtre principale
        self.clicked.connect(self.main_window.ajoute_buildingsquare)  # Connectez le clic à la méthode de la fenêtre principale
        self.setFixedSize(50, 50)  # taille du widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Définir les points du square
        points = [QPointF(0, 0), QPointF(self.width(), 0), QPointF(self.width(), self.height()), QPointF(0, self.height())]

        # On crée le squaree
        square_polygon = QPolygonF(points)

       # on dessine
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.black))
        painter.drawPolygon(square_polygon)