import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QToolBar, QAction, QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QIcon
from PyQt5.QtCore import Qt, QPointF


class MaSceneGraphique(QGraphicsScene):
    def __init__(self, parent=None):
        super(MaSceneGraphique, self).__init__(parent)
        self.est_carre_selectionne = False
        self.est_triangle_selectionne = False

    def mousePressEvent(self, event):
        # Gérer les événements de clic pour sélectionner/désélectionner les formes
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if isinstance(item, QGraphicsRectItem):
            self.est_carre_selectionne = not self.est_carre_selectionne
        elif isinstance(item, QGraphicsPolygonItem):
            self.est_triangle_selectionne = not self.est_triangle_selectionne
        else:
            # Désélectionner toutes les formes si on clique à l'extérieur
            self.est_carre_selectionne = False
            self.est_triangle_selectionne = False

        super(MaSceneGraphique, self).mousePressEvent(event)


class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(MaFenetrePrincipale, self).__init__()

        self.initUI()

    def initUI(self):
        # Créer une instance de MaSceneGraphique
        self.scene = MaSceneGraphique(self)

        # Créer une vue pour la scène graphique
        self.vue = QGraphicsView(self.scene)
        self.setCentralWidget(self.vue)

        # Créer la barre d'outils
        self.creerBarreOutils()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.showFullScreen()

    def creerBarreOutils(self):
        # Créer la barre d'outils
        barre_outils = QToolBar("Barre d'outils")
        self.addToolBar(barre_outils)

        # Ajouter des actions à la barre d'outils
        # Action pour dessiner juste un carré avec une icône standard
        action_carre = QAction(QIcon.fromTheme("document-new"), 'Ajoute un carré', self)
        action_carre.triggered.connect(self.dessinerCarre)
        barre_outils.addAction(action_carre)

        # Action pour ajouter un triangle avec une icône standard
        action_triangle = QAction(QIcon.fromTheme("document-open"), 'Ajouter un triangle', self)
        action_triangle.triggered.connect(self.ajouterTriangle)
        barre_outils.addAction(action_triangle)

    def dessinerCarre(self):
        # Dessiner juste un carré sur la scène
        carre_item = self.scene.addRect(0, 0, 50, 50)
        carre_item.setPos(50, 50)
        carre_item.setBrush(QBrush(Qt.red))
        carre_item.setPen(QPen(Qt.black))
        carre_item.setFlag(QGraphicsRectItem.ItemIsMovable)

    def ajouterTriangle(self):
        # Ajouter un triangle à la scène
        # Utiliser QPolygonF avec QPointF pour définir les points du triangle
        triangle_item = self.scene.addPolygon(QPolygonF([QPointF(0, 0), QPointF(30, 0), QPointF(15, -50)]))
        triangle_item.setPos(150, 50)
        triangle_item.setBrush(QBrush(Qt.cyan))
        triangle_item.setPen(QPen(Qt.black))
        triangle_item.setFlag(QGraphicsPolygonItem.ItemIsMovable)

        # Définir l'angle de rotation pour le triangle (en degrés)
        triangle_item.setRotation(0) # Vous pouvez ajuster l'angle selon vos besoins


def main():
    app = QApplication(sys.argv)
    fenetre = MaFenetrePrincipale()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()