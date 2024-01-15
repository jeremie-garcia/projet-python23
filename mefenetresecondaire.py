
from PyQt5.QtWidgets import  QComboBox, QDialog, QGraphicsView,QVBoxLayout,QHBoxLayout,QLabel, QLineEdit,QWidget, QSlider, QApplication,QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar,QGraphicsItem



class MaFenetreSecondaire(QDialog):
    def __init__(self, VehiculeItem):
        super(MaFenetreSecondaire, self).__init__()

        self.setWindowTitle("Drone Details")
        self.setGeometry(100, 100, 300, 150)

        # label avec le nom du drone
        name_label = QLabel(f"Drone ID: {VehiculeItem.drone.ID}")
        # Permet de changer l'ID du drone
        self.name_line_edit = QLineEdit(VehiculeItem.drone.ID)
        self.name_line_edit.textChanged.connect(VehiculeItem.update_drone_ID)

        
        # Menu déroulant avec la couleur
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(['Cyan', 'Green', 'Blue', 'Yellow', 'Purple','Red'])
        self.color_combobox.setCurrentIndex(0)
        self.color_combobox.currentIndexChanged.connect(VehiculeItem.update_drone_color)
       

        #boutton ok
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

       # mets en place les layouts
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.color_combobox)
        layout.addWidget(ok_button)
        
        # Initialisation classique
        self.setLayout(layout)   
        self.show()
