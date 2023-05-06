import random

class Hangar:
    def __init__(self, type):
        self.x = "%.2f" % random.uniform(-100, 100)
        self.y = "%.2f" % random.uniform(-100, 100)
        self.available = True
        self.type = type
        self.plane = None
        # TODO: ADICIONAR ID DO HANGAR E AVIAO O ESTA A OCUPAR

    def get_coords(self):
        return self.x, self.y

    def get_availability(self):
        return self.available

    def set_plane(self, plane):
        self.available = False
        self.plane = plane


    def __str__(self):
        return f'''***** HANGAR
\t X: {self.x}
\t Y: {self.y}
\t AVAILABLE: {self.available}
\t TYPE: {self.type}
        *****'''
