import json
class Building:
    def __init__(self,ID,vertices): # liste des positions des points (x,y,z))
        self.ID = ID #chaine de caractère
        self.vertices = vertices #liste de liste de points réels x : position horizontal (0-5m),y: position vertical(0-5m),z  :altitude (0-10m)

class Drone:
    def __init__(self, ID, position, goal, orientation ,source_strength=0.5, imag_source_strength=0.5, sink_strength=5, safety=0.0001):
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
        self.drone=[] #liste de drones

    def add_building(self,build):
        self.buildings.append(build) #ajout de building

    def add_drone(self,vehicles):
        self.drone.append(vehicles) #ajout de drone

    def json(self,cases_name): #cases_key = nom de la 'cases' du json 
        buildings_json = [{'ID': Building.ID, 'vertices': Building.vertices} for Building in self.buildings] #dictionnaire avec les atributs du building (name et verticie)
        drones_json = [{'ID': Drone.ID, 'position': Drone.position, 'goal': Drone.goal, 'orientation' : Drone.orientation, 'source_strength': Drone.source_strength, 'imag_source_strength' : Drone.imag_source_strength, 'sink_strength': Drone.sink_strength, 'safety': Drone.safety} for Drone in self.drone]
        dico={cases_name: {'buildings': buildings_json, 'vehicles': drones_json}} #dictionnaire de dictionnaire avec cases_name en clé principale et les dictionnaires drones et buildings
        with open('data.json','w') as file:
            json.dump(dico, file, indent=2) #ouvrir et enregistrer la liste de dictionnaire dans un fichier json
        
# Exemple :
ex= Modele()
ex.add_building(Building('Building1',[[0.29, -0.40, 1.2],[-0.29, -0.40, 1.2],[-0.47, 0.15, 1.2],[0, 0.5, 1.2]]))
ex.add_building(Building('Building2', [[0.58, -5.4, 1.2],[-0.58, -1.39,1.2],[-0.59, -0.25, 1.2],[-0.58, 0.22, 1.2]]))
ex.add_drone(Drone('Drone1', [0, 0, 0], [1, 1, 1],0, 0.5, 0.5, 5, 0.0001))
ex.add_drone(Drone('Drone2', [0, 0, 0], [1, 1, 1],0, 0.5, 0.5, 5, 0.0001))
Modele.json(ex,'default')

