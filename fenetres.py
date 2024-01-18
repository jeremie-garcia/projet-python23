from PyQt5.QtWidgets import  QSpacerItem, QSizePolicy,QSlider, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QGraphicsView, QMainWindow, QPushButton, QDialog, QComboBox
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt

from gflow.utils.plot_utils import PlotTrajectories
from gflow.cases import Cases
from gflow.utils.simulation_utils import run_simulation

import scenegraphique
import modele
import buttons
import items

import numpy as np



ang_drone=0
ang_goal=0



class MaFenetrePrincipale(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
 
        self.scene = scenegraphique.MaSceneGraphique(self)
        self.vue = QGraphicsView(self.scene)
        self.vue.scale(1, -1)    # permet de retouner l'axe y pour coller avec les axes de la volières
        self.vue.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
 
        self.drone_index=60
        self.building_index=1
 
        self.button_json = QPushButton('créer json')
        self.gflow_button = QPushButton('lancer gflow')  
        

        # Créer un layout principal
        mainlayout = QHBoxLayout()
 
        # Ajouter layout1 à gauche
        layoutLeft = self.create_layoutLeft()  
        mainlayout.addLayout(layoutLeft)
 
        # Ajouter la scène graphique à droite
        mainlayout.addWidget(self.vue)
 
        # Créer le widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainlayout)
        self.setCentralWidget(centralWidget)
 
        self.setGeometry(100, 100, 800, 600)  # taille de la fenetre qui s'ouvre
        self.setWindowTitle('Application avec Barre d\'Outils et Scène Graphique')
        self.model = modele.Modele()
        self.button_json.clicked.connect(self.creer_json)
 

        self.gflow_button.clicked.connect(gflow)
 
        self.liste_vehicle_item = {}
 
        self.show()
 

    def create_layoutLeft(self):
        LayoutLeft = QVBoxLayout()
 
       
 # Créer les layouts
        h1_layout = QHBoxLayout()
        h2_layout = QHBoxLayout()
        h3_layout = QHBoxLayout()
 
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
 
        # ajouter espace extensible gauche
        h1_layout.addItem(spacer_left)
        
        # Ajouter le widget au centre (par exemple, un bouton)
        label_triangle = QLabel ('ajouter un drone')
        triangle_widget = buttons.TriangleButton(self)
        h1_layout.addWidget(triangle_widget)
        h1_layout.addWidget(label_triangle)
        
        # Ajouter un espace extensible droite
        h1_layout.addItem(spacer_right)
 
        LayoutLeft.addLayout(h1_layout)
 
        # ajouter espace à gauche
        h2_layout.addItem(spacer_left)
        
        # Ajouter le square à notre layout
        label_square = QLabel ('ajouter un building square')
        square_widget = buttons.SquareButton(self)
        h2_layout.addWidget(square_widget)
        h2_layout.addWidget(label_square)
        
        # ajouter espace à droite
        h2_layout.addItem(spacer_right)
 
        LayoutLeft.addLayout(h2_layout)
 
        # ajouter espace à gauche
        h3_layout.addItem(spacer_left)
        
        # Ajouter l'hexagone a notre layout
        label_hexa = QLabel ('ajouter un building hexagonal')
        hexa_widget = buttons.HexagonButton(self)
        h3_layout.addWidget(hexa_widget)
        h3_layout.addWidget(label_hexa)
        
        # ajouter espace à droite
        h3_layout.addItem(spacer_right)
       
        LayoutLeft.addLayout(h3_layout)
       
 
        # Ajouter des boutons de zoom à votre layout personnalisé
        zoom_in_button = buttons.ZoomButtonP('ZoomButtonP.jpg', 2 , self ,'Zoom In')
        zoom_out_button = buttons.ZoomButtonN('ZoomButtonN.jpg', 0.5, self , 'Zoom Out')
        LayoutLeft.addWidget(zoom_in_button)
        LayoutLeft.addWidget(zoom_out_button)

     
        # boutton json
        LayoutLeft.addWidget(self.button_json)
 

        # boutton Jflow
        gflow_button = QPushButton('lacer jflow')
        LayoutLeft.addWidget (self.gflow_button)
       
       
        self.button_json.clicked.connect(self.creer_json) # Exécute la fonction qui créer le fichier json
 
        return LayoutLeft
 
    #Suite a de nombreux problèmes avec l'invertion de l'axe y, on a eu des problèmes avec le zoom, aide grace à internet pour resoudre le problème
    # https://doc.qt.io/qtforpython-5/PySide2/QtGui/QTransform.html#PySide2.QtGui.PySide2.QtGui.QTransform.m11
    
    def zoom(self, facteur):
        echelle_actuelle = self.vue.transform().m11() # echelle de la vue actuelle
        nouvelle_echelle = echelle_actuelle * facteur # multiplie par un facteur de zoom
        
        # permet de conserver l'invertion de l'axe y avec comme point d'ancrage le centre de la volière
        #déplace le centre de la vue vers le centre de la fenêtre.
        # applique la nouvelle échelle avec facteur negatif sur le y pour l'inversion
        
        self.vue.setTransform(QTransform().translate(self.vue.viewport().width() / 2, self.vue.viewport().height() / 2).scale(nouvelle_echelle, -nouvelle_echelle))
    def zoom_out(self, facteur):
        echelle_actuelle = self.vue.transform().m11()
        nouvelle_echelle = echelle_actuelle * facteur
        self.vue.setTrans
 
   
    def creer_json(self):
        self.model.json('fichierjson')
 
       
    def update_drone_data(self, AC_ID, pos_x, pos_y,pos_z, quat_a, quat_b, quat_c, quat_d):
        if( str(AC_ID) in self.liste_vehicle_item.keys()):
            item_drone = self.liste_vehicle_item[str(AC_ID)]
            modele_drone = item_drone.drone
            modele_drone.position=(pos_x*100,pos_y*100,pos_z*100)
        

            quat = [quat_a,quat_b,quat_c,quat_d]
            quat= quat/ np.linalg.norm(quat)        #normalisation du quaterion
            yaw = np.arctan2(2 * (quat_a*quat_b + quat_c*quat_d), 1 - 2 * (quat_b**2 + quat_c**2))  #mouvement lacet
            modele_drone.orientation = np.degrees(yaw)

            
            item_drone.update_position()



    def ajoute_drone(self):
        #creer un drone au centre
        drone = modele.Drone(str(self.drone_index), [0,0,0],[0,0,0], ang_drone)
        self.model.add_drone(drone)
 
        droneItem = items.VehicleItem(drone, self)
        
        goalItem = items.GoalItem(drone)
        droneItem.goalItem = goalItem
        self.scene.addItem(droneItem)
        self.scene.addItem(goalItem)
 
        #stocker dans le dictionnaire
        self.liste_vehicle_item[drone.ID] = droneItem
 
        # Permet que chaque drone est une ID différente
        self.drone_index+=1




   
    def ajoute_buildingsquare(self):
        # créer un batiment square au centre
        vertices=[[0,0,151.5],[0,60.5,151.5],[60.50,60.5,151.5],[60.5,0,151.5]]
        building = modele.Building("building" + str(self.building_index),vertices)
        self.model.add_building(building)
 
        buildingItem = items.ObstacleItem(building, self)
        self.scene.addItem(buildingItem)
        self.building_index+=1
 

    def ajoute_buildinghexa(self):
        # créer un batiment hexagonal au centre
        vertices=[[60,0,151.5],[30,51.96,151.5],[-30,51.96,151.5],[-60,0,151.5],[-30,-51.96,151.5],[30,-51.96,151.5]]
        building = modele.Building("building" + str(self.building_index),vertices)
        self.model.add_building(building)
 
        buildingItem = items.ObstacleItem(building,self)
        self.scene.addItem(buildingItem)
        self.building_index+=1
 

def gflow():                           # on a reprit votre fichier main_gflow 
    file_name = "data.json"
    case_name = "fichierjson"

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
 
   
 

class MaFenetreSecondaireGoal(QDialog):
    def __init__(self, vehicleItem):
        super(MaFenetreSecondaireGoal, self).__init__()
 
        self.setWindowTitle("Goal Details")
        self.setGeometry(100, 100, 300, 150)
 
        # label avec le nom du Goal
        name_label = QLabel(f"Goal ID: {vehicleItem.drone.ID}")
        # On ne permet pas de changer le nom du goal car il change automatiquement avec celui du drone
 
        # Affichage de l'altitude
        altitude_display = QLabel (f"Goal altitude :{vehicleItem.drone.goal[2]}")
        # Slider pour l'altitude
        altitude_slider = QSlider(Qt.Horizontal)
        altitude_slider.setMinimum(0)
        altitude_slider.setMaximum(800)
        altitude_slider.setValue(vehicleItem.drone.goal[2])
        altitude_slider.valueChanged.connect(vehicleItem.update_goal_altitude) # Exécute la fonction qui modifie le modèle
        altitude_slider.valueChanged.connect(lambda val : altitude_display.setText(f"Goal altitude :{val}")) # Permet de mettre à jour l'affichage
  
        # # changer la couleur:
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(['Cyan', 'Green', 'Blue', 'Yellow', 'Purple','Red'])
        self.color_combobox.setCurrentIndex(0)
        self.color_combobox.currentIndexChanged.connect(vehicleItem.update_goal_color)

        #boutton ok
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept) # méthode accept de la classe Qdialog qui accepte les changements et ferme la fenetre
       
       # mets en place les layouts
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(altitude_display)
        layout.addWidget(altitude_slider)
        layout.addWidget(self.color_combobox)
        layout.addWidget(ok_button)
 
        # Initialisation classique
        self.setLayout(layout)  
        self.show()

        

class MaFenetreSecondaireBuilding(QDialog):
    def __init__(self, buildingItem,fenetre):
        super(MaFenetreSecondaireBuilding, self).__init__()
 
        self.setWindowTitle("Buildings Details")
        self.setGeometry(100, 100, 300, 150)
 
        # label avec le nom du Building
        name_label = QLabel(f"Building ID: {buildingItem.building.ID}")

 
        #Affichage de l'altidude
        altitude_display = QLabel (f"Building altitude :{buildingItem.building.vertices[0][2]}")
        # Slideer de l'altitude
        altitude_slider = QSlider(Qt.Horizontal)
        altitude_slider.setMinimum(0)
        altitude_slider.setMaximum(800)
        altitude_slider.setValue(int(buildingItem.building.vertices[0][2]))
        altitude_slider.valueChanged.connect(buildingItem.uptade_building_altitude) #Exécute la fonction qui modifie le modele
        altitude_slider.valueChanged.connect(lambda val : altitude_display.setText(f"Building altitude :{val}")) # Permet de mettre à jour l'affichage
 
        
        #boutton ok
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept) # méthode accept de la classe Qdialog qui accepte les changements et ferme la fenetre


       # mets en place les layouts
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(altitude_display)
        layout.addWidget(altitude_slider)
        layout.addWidget(ok_button)
 
       
        # Initialisation classique du layout
        self.setLayout(layout)  
        self.show()

        # model = fenetre.model
 

class MaFenetreSecondaireDrone(QDialog):
    def __init__(self, vehicleItem, fenetre):
        super(MaFenetreSecondaireDrone, self).__init__()
 
        self.setWindowTitle("Drone Details")
        self.setGeometry(100, 100, 300, 150)
        # label avec le nom du drone
        name_label = QLabel(f"Drone ID: {vehicleItem.drone.ID}")
        
        # Permet de changer l'ID du drone
        self.name_line_edit = QLineEdit(vehicleItem.drone.ID)
        self.name_line_edit.textChanged.connect(vehicleItem.update_drone_ID)
 
       
        # Menu déroulant avec la couleur
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(['Cyan', 'Green', 'Blue', 'Yellow', 'Purple','Red'])
        self.color_combobox.setCurrentIndex(0)
        self.color_combobox.currentIndexChanged.connect(vehicleItem.update_drone_color) # execute la fonction qui change la couleur de l'item drone

 
        # Boutton pour enlever le drone:
        remove_button = QPushButton ("retirer le drone")

        model = fenetre.model
        remove_button.clicked.connect(lambda : model.remove_drone(vehicleItem.drone.ID)) # Exécute la fonction qui retire le drone du modele
        remove_button.clicked.connect(lambda : fenetre.scene.removeItem(vehicleItem)) # retire la vue graphique du drone de la scene
        remove_button.clicked.connect(lambda : fenetre.scene.removeItem(vehicleItem.goalItem)) # retire la vue graphique de la cible de la scene
  
 
       
 
        #boutton ok
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept) # méthode accept de la classe Qdialog qui accepte les changements et ferme la fenetre
 
       # mets en place les layouts
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.color_combobox)
        layout.addWidget(remove_button)
        layout.addWidget(ok_button)
       
        # Initialisation classique du layout
        self.setLayout(layout)  
        self.show()
