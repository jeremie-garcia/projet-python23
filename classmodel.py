class Building:
    def __init__(self,name,verticies):
        self.name = name
        self.verticies = verticies



class Drone:
    def __init__(self, name, posit, target, orient):
        self.name = name
        self.posit = posit
        self.target = target
        self.orient = orient



class Modele:
    def __init__(self):
        self.builings=[]
        self.drones=[]

    def add_building(self,build):
        self.buildings.append(build)

    def add_drone(self,drone):
        self.drones.append(drone)
