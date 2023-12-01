class Building:
    def __init__(self,name,verticies):
        self.id = name
        self.verticies = verticies



class Vehicule:
    def __init__(self, name, posit, target, orient):
        self.id = name
        self.posit = posit
        self.target = target
        self.orient = orient



class Modele:
    def __init__(self):
        self.builings=[]
        self.vehicules=[]

    def add_building(self,build):
        self.buildings.append(build)

    def add_vehicule(self,vehic):
        self.vehicules.append(vehic)