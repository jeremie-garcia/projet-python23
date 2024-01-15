
from PyQt5.QtWidgets import  QSpacerItem, QSizePolicy, QGraphicsView,QVBoxLayout,QHBoxLayout,QLabel, QLineEdit,QWidget, QSlider, QApplication,QApplication, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsView, QMainWindow, QPushButton, QToolBar, QGraphicsRectItem, QGraphicsPolygonItem,QToolBar,QGraphicsItem
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt
from gflow.utils.plot_utils import PlotTrajectories
from gflow.cases import Cases
from gflow.utils.simulation_utils import run_simulation
import scenegraphique
import modele
import boutons
import items
import main



ang_drone=180
ang_goal=180



class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.scene = scenegraphique.MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.vue.scale(1, -1)
        self.vue.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio) 

        self.drone_index=60

        self.button_jason = QPushButton('créer Jason')
        self.gflow_button = QPushButton('lancer gflow')        
        # Créer un layout principal
        mainlayout = QHBoxLayout()

        # Ajouter layout1 à gauche
        layoutLeft = self.create_layoutLeft()  # Vous devriez implémenter votre propre fonction pour créer layout1
        mainlayout.addLayout(layoutLeft)

        # Ajouter la scène graphique à droite
        mainlayout.addWidget(self.vue)

        # Créer le widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainlayout)
        self.setCentralWidget(centralWidget)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.model = modele.Modele()
        self.button_jason.clicked.connect(self.creer_json)


        self.gflow_button.clicked.connect(gflow)

        self.liste_vehicle_item = {}

        self.show()


    def create_layoutLeft(self):
        LayoutLeft = QVBoxLayout()

        # Ajoutez des widgets à la mise en page

        h1_layout = QHBoxLayout()
        h2_layout = QHBoxLayout()
        h3_layout = QHBoxLayout()
        h4_layout = QHBoxLayout()

        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ajouter espace extensible gauche
        h1_layout.addItem(spacer_left)
        # Ajouter le widget au centre (par exemple, un bouton)
        label_triangle = QLabel ('ajouter un drone')
        triangle_widget = boutons.TriangleWidget(self)
        h1_layout.addWidget(triangle_widget)
        h1_layout.addWidget(label_triangle)
        # Ajouter un espace extensible droite
        h1_layout.addItem(spacer_right)
  
        LayoutLeft.addLayout(h1_layout)

        # ajouter espace à gauche
        h2_layout.addItem(spacer_left)
        # Ajouter le carree à notre layout 
        label_carree = QLabel ('ajouter un building carré')
        carree_widget = boutons.CarreeWidget(self)
        h2_layout.addWidget(carree_widget)
        h2_layout.addWidget(label_carree)
        # ajouter espace à droite
        h2_layout.addItem(spacer_right)

        LayoutLeft.addLayout(h2_layout)

        

        
        # ajouter espace à gauche
        h3_layout.addItem(spacer_left)
        # Ajouter l'hexagone a notre layout
        label_hexa = QLabel ('ajouter un building hexagonal')
        hexa_widget = boutons.HexagonWidget(self)
        h3_layout.addWidget(hexa_widget)
        h3_layout.addWidget(label_hexa)
        # ajouter espace à droite
        h3_layout.addItem(spacer_right)
        
        LayoutLeft.addLayout(h3_layout)
        

        #  # Ajouter des boutons de zoom à votre layout personnalisé
        zoom_in_button = boutons.ZoomButtonP('ZoomButtonP.jpg', 2 , self ,'Zoom In')
        zoom_out_button = boutons.ZoomButtonN('ZoomButtonN.jpg', 0.5, self , 'Zoom Out')
        LayoutLeft.addWidget(zoom_in_button)
        LayoutLeft.addWidget(zoom_out_button)

     
        # boutton jason
        LayoutLeft.addWidget(self.button_jason)

  

        # boutton Jflow
        gflow_button = QPushButton('lacer jflow')
        LayoutLeft.addWidget (self.gflow_button)
        
        
        # self.button_jason.clicked.connect(self.creer_json)

        return LayoutLeft

    def zoom(self, facteur):
        echelle_actuelle = self.vue.transform().m11()
        nouvelle_echelle = echelle_actuelle * facteur
        self.vue.setTransform(QTransform().translate(self.vue.viewport().width() / 2, self.vue.viewport().height() / 2).scale(nouvelle_echelle, -nouvelle_echelle))
    def zoom_out(self, facteur):
        echelle_actuelle = self.vue.transform().m11()
        nouvelle_echelle = echelle_actuelle * facteur
        self.vue.setTrans

    def creer_json(self):
        modele = main.Modele
        modele.json('fichier jason')

        
    def update_drone_data(self, AC_ID, pos_x, pos_y,pos_z, quat_a, quat_b, quat_c, quat_d):
        item_drone = self.liste_vehicle_item[AC_ID]
        modele_drone = item_drone.drone
        modele_drone.position=(pos_x,pos_y,pos_z)
        item_drone.update_position()



    def ajoute_drone(self):
        #creer un drone
        drone = modele.Drone(str(self.drone_index), [0,0,0],[0,0,0], ang_drone)
        self.model.add_drone(drone)

        droneItem = items.VehiculeItem(drone)
        goalItem = items.GoalItem(drone)
        self.scene.addItem(droneItem)
        self.scene.addItem(goalItem)

        #stocker dans le dictionnaire
        self.liste_vehicle_item[drone.ID] = droneItem

        #change le nom pour le prochain drone
        self.drone_index+=1
    
    def ajoute_buildingcarre(self):
        vertices=[[0,0,151.5],[0,60.5,151.5],[60.50,60.5,151.5],[60.5,0,151.5]]
        building = modele.Building("OBScarré",vertices)
        self.model.add_building(building)

        buildingItem = items.ObstacleItem(building)
        self.scene.addItem(buildingItem)


    def ajoute_buildinghexa(self):
        vertices=[[60,0,151.5],[30,51.96,151.5],[-30,51.96,151.5],[-60,0,151.5],[-30,-51.96,151.5],[30,-51.96,151.5]]
        building = modele.Building("OBShexa",vertices)
        self.model.add_building(building)

        buildingItem = items.ObstacleItem(building)
        self.scene.addItem(buildingItem)


def gflow():
    file_name = "data.json"
    case_name = "fichier jason"

    case = Cases.get_case(file_name=file_name, case_name=case_name)

    run_simulation(
        case,
        t=2000,  # maximum number of timesteps
        update_every=1,  # leave as 1
        stop_at_collision=False,  # leave as False
        max_avoidance_distance=999999,  # larger than simulation domain
    )

    trajectory_plot = PlotTrajectories(case, update_every=1)
    trajectory_plot.show()

    




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
