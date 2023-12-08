import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QToolBar, QAction, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QIcon
from PyQt5.QtCore import Qt, QPointF
import Classmodele as cm

v1 = cm.Vehicule('v1',[20,20,20],[300,300,20],0)

class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)
        self.est_carre_selectionne = False
        self.est_triangle_selectionne = False

class Q_graphical_item(cm.Vehicule,cm.Building):

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
        triangle_item.setRotation(0) # Vous pouvez ajuster l'angle selon vos besoins



class MaFenetrePrincipale(QMainWindow,Q_graphical_item):
    def __init__(self):
        super(MaFenetrePrincipale, self,).__init__() # arg de Q_graphical_items
        

        self.initUI()

    def initUI(self):
        # Créer une instance de MaSceneGraphique
        self.scene = MaSceneGraphique(self)

        # Créer une vue pour la scène graphique
        self.vue = QGraphicsView(self.scene)
        self.setCentralWidget(self.vue)

        # Créer la barre d'outils
        #self.creerBarreOutils()
        
        self.ajouterTriangle()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.showFullScreen()






def main():
    app = QApplication(sys.argv)
    fenetre = MaFenetrePrincipale()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
