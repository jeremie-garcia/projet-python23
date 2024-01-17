import json
import numpy as np

class Building:
    def __init__(self,ID,vertices): # liste des positions des points (x,y,z))
        self.ID = ID #chaine de caractère
        self.vertices = vertices #liste de liste de points réels x : position horizontal (-4, 4m), y: position vertical(-4,4m), z :altitude (0-8m)

class Drone:
    def __init__(self, ID, position, goal, orientation ,source_strength=0.5 , imag_source_strength=0.5, sink_strength=5, safety=0.0001):
        self.ID = ID #chaine de caractère
        self.position = position #liste de 3 points x,y,z
        self.goal = goal #liste de 3 points x,y,z
        self.orientation=orientation #angle en degrès
        self.source_strength = source_strength #valeur fixe :0.5
        self.imag_source_strength = imag_source_strength #valeur fixe : 0.5
        self.sink_strength=sink_strength #valeur fixe : 5
        self.safety=safety #valeur fixe :0.0001
        
class Modele:
    def __init__(self):
        self.buildings=[] #liste de building
        self.drones=[] #liste de drones

    def add_building(self,build):
        self.buildings.append(build) #ajout de building dans une liste

    def remove_building(self,build_id):
        self.buildings = [b for b in self.buildings if b.ID != build_id] #suppression de building d'une liste


    def add_drone(self,vehicles):
        self.drones.append(vehicles) #ajout de drone dans une liste

    def remove_drone(self,drone_id):
        self.drones = [d for d in self.drones if d.ID != drone_id] #suppression de drone dans une liste

    def json(self,cases_name): #cases_key = nom de la 'cases' du json 
        buildings_json = [{'ID': Building.ID, 'vertices': (np.array(Building.vertices)/100).tolist()} for Building in self.buildings] #on divise par 100 les vertices pour être en mètre
        drones_json = [{'ID': Drone.ID, 'position': (np.array(Drone.position)/100).tolist(), 'goal': (np.array(Drone.goal)/100).tolist(), 'orientation' : Drone.orientation, 'source_strength': Drone.source_strength, 'imag_source_strength' : Drone.imag_source_strength, 'sink_strength': Drone.sink_strength, 'safety': Drone.safety} for Drone in self.drones]
        dico={cases_name: {'buildings': buildings_json, 'vehicles': drones_json}} 
        with open('data.json','w') as file:
            json.dump(dico, file, indent=2) #ouvrir et enregistrer la liste de dictionnaire dans un fichier json
        

Modele.json(Modele(),'fichierjson')
