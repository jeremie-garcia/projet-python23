from PyQt5.QtWidgets import QGraphicsSceneMouseEvent,  QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF
import math
import maindrone
import fenetres
 

class ObstacleItem(QGraphicsPolygonItem):           #définir les obstacles
    def __init__(self,building):
 
        self.building = building
        self.building_ID = self.building.ID
        self.polygonpoints=[]
        #pour chaque vertices (x,y,z) je cree un point QTpointf et j'ajoute dans la liste
        for vertice in building.vertices:
            self.polygonpoints.append(QPointF(vertice[0],vertice[1]))      
           
 
        self.polygone = QPolygonF( self.polygonpoints )         #défini le polygone avec ses points
       
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
       
        self.setBrush(QBrush(Qt.red))                        #le dessine
        self.setPen(QPen(Qt.red))
        maindrone.Modele.add_building(self.building)          #l'ajoute au modèle
 
    # def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
    #     print("press", event)
   
    # def mouseMoveEvent(self, event):
    #     #quand on bouge alors on change la position du drone
    #     self.newx=event.scenePos().x()                                #je recupere la position de la souris
    #     self.newy=event.scenePos().y()
       
    #     self.update_position()
        
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.RightButton:
         
            self.details_dialog = fenetres.MaFenetreSecondaireBuilding(self)
            self.details_dialog.show()
 
        elif event.button() == Qt.LeftButton:
            # Left mouse button is pressed
            self.handle_left_button_press(event)
 
    def handle_right_button_press(self, event):
        # Handle right mouse button press
        pass
 
    def handle_left_button_press(self, event):
        # Handle left mouse button press
        pass
 
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            # Right mouse button is being held down
            self.handle_left_button_held(event)
           
 
    def handle_left_button_held(self, event):
        # Handle right mouse button being held down
        
        self.newx=event.scenePos().x()                                #je recupere la position de la souris
        self.newy=event.scenePos().y()
        self.update_position()
        # print("press", event)
 
        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
 
       
    def update_position(self):
        #self.setRotation(self.drone.orient)
        nbs_sommets=len(self.building.vertices)
        if nbs_sommets == 4:                            # calcul des coordonées en fonctions de carré ou hexa
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

    def uptade_building_altitude (self, new_alt):
        nbs_sommets=len(self.building.vertices)
        for i in range (nbs_sommets):
            self.building.vertices[i][2] = new_alt



class VehicleItem(QGraphicsPolygonItem):
    def __init__(self,vehicle):
 
        self.drone = vehicle
        self.x1= vehicle.position[0] + 25            #je défini les points du triangle, centré
        self.y1= vehicle.position[1] - 25
        self.x2= vehicle.position[0] - 25
        self.y2= vehicle.position[1] - 25
        self.x3= vehicle.position[0]
        self.y3=vehicle.position[1] + 25
        self.polygone = QPolygonF([                              #je fais un polygone triangle
                        QPointF(self.x1, self.y1),
                        QPointF(self.x2, self.y2 ),
                        QPointF(self.x3, self.y3)
                    ])
       
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
       
        # self.color_index = ['Red','Green','Blue','Yellow','Purple','Cyan']
        self.color_dict =  {'Red': Qt.red, 'Green': Qt.green, 'Blue': Qt.blue, 'Yellow': Qt.yellow, 'Purple': Qt.magenta, 'Cyan':Qt.cyan}
        self.setRotation(self.drone.orientation)
        self.setBrush(QBrush(self.color_dict['Green']))
        self.setPen(QPen(self.color_dict['Green']))
        maindrone.Modele.add_drone(self.drone)
        # self.scene = scene  # Ajoutez une référence à la scène
        # self.view = scene.views()[0]  # Obtenez la vue associée à la scène



    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.RightButton:
         
 
            self.details_dialog = fenetres.MaFenetreSecondaireDrone(self)
            self.details_dialog.show()
 
        elif event.button() == Qt.LeftButton:
            # Left mouse button is pressed
            self.handle_left_button_press(event)
 
    def handle_right_button_press(self, event):
        # Handle right mouse button press
        pass
 
    def handle_left_button_press(self, event):
        # Handle left mouse button press
        pass
 
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            # Right mouse button is being held down
            self.handle_left_button_held(event)
           
 
    def handle_left_button_held(self, event):
        # Handle right mouse button being held down
        self.newx=event.scenePos().x()                                #je recupere la position de la souris
        self.newy=event.scenePos().y()
        self.update_position()
        # print("press", event)
 
        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
       
    def update_position(self):
        self.setRotation(self.drone.orientation)
        self.drone.position[0]=self.newx
        self.drone.position[1]=self.newy
        self.setPos(QPointF(self.newx, self.newy))                  #ca deplace le drone dans l'interface
        #print(self.drone.target)
 
    def update_drone_color(self):
        color_name = self.details_dialog.color_combobox.currentText()
        self.setBrush(QBrush(self.color_dict.get(color_name, Qt.cyan)))
        self.setPen(QPen(self.color_dict.get(color_name, Qt.cyan)))
 
    def update_goal_color(self):
        color_name = self.details_dialog.color_combobox.currentText()
        GoalItem.setBrush(QBrush(self.color_dict.get(color_name, Qt.cyan)))
        GoalItem.setPen(QPen(self.color_dict.get(color_name, Qt.cyan)))



    def update_drone_ID(self, new_text):
        self.drone.ID = new_text
 

class GoalItem(QGraphicsPolygonItem):
    def __init__(self,vehicle):
 
        self.drone = vehicle
        self.x1 = vehicle.position[0]        #points du triangle pour la cible
        self.y1 = vehicle.position[1] + 30
        self.x2 = vehicle.position[0] + 5
        self.y2 = vehicle.position[1] + 5
        self.x3 = vehicle.position[0] + 30
        self.y3 = vehicle.position[1]
        self.x4 = vehicle.position[0] + 5      
        self.y4 = vehicle.position[1] - 5
        self.x5 = vehicle.position[0]
        self.y5 = vehicle.position[1] - 30
        self.x6 = vehicle.position[0] - 5
        self.y6 = vehicle.position[1] - 5
        self.x7 = vehicle.position[0] - 30    
        self.y7 = vehicle.position[1]
        self.x8 = vehicle.position[0] - 5
        self.y8 = vehicle.position[1] + 5
 
        self.polygone = QPolygonF([                              #je fais un polygone triangle
                        QPointF(self.x1, self.y1),
                        QPointF(self.x2, self.y2),
                        QPointF(self.x3, self.y3),
                        QPointF(self.x4, self.y4),
                        QPointF(self.x5, self.y5),
                        QPointF(self.x6, self.y6),
                        QPointF(self.x7, self.y7),
                        QPointF(self.x8, self.y8)
                    ])
       
        super(QGraphicsPolygonItem,self).__init__(self.polygone)
       
        self.setRotation(self.drone.orientation)
        self.setBrush(QBrush(Qt.green))
        self.setPen(QPen(Qt.green))
 
    def update_goal_altitude (self, new_alt):
        self.drone.goal[2] = new_alt
       
 
       
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.RightButton:
         
            self.details_dialog = fenetres.MaFenetreSecondaireGoal(self)
            self.details_dialog.show()
 
        elif event.button() == Qt.LeftButton:
            # Left mouse button is pressed
            self.handle_left_button_press(event)
 
    def handle_right_button_press(self, event):
        # Handle right mouse button press
        pass
 
    def handle_left_button_press(self, event):
        # Handle left mouse button press
        pass
 
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            # Right mouse button is being held down
            self.handle_left_button_held(event)
           
 
    def handle_left_button_held(self, event):
        # Handle right mouse button being held down
        
        self.drone.goal[0]=event.scenePos().x()                                #je recupere la position de la souris
        self.drone.goal[1]=event.scenePos().y()
        self.update_position()
        # print("press", event)
 
        #self.drone.set_position(evt.scenePos().x(), evt.scenePos().y())
 
       
    def update_position(self):
        self.setRotation(self.drone.orientation)
 
        self.setPos(QPointF(self.drone.goal[0], self.drone.goal[1]))                  
        #print(self.drone.goal)
 
