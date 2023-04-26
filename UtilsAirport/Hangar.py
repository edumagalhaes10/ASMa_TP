import random

class Hangar:
    def __init__(self, type):
        self.x = "%.2f" % random.uniform(-100, 100)
        self.y = "%.2f" % random.uniform(-100, 100)
        self.available = True
        self.type = type

    def get_coords(self):
        return self.x, self.y

    def get_availability(self):
        return self.available

    def __str__(self):
        return f'''***** HANGAR
X: {self.x}
Y: {self.y}
AVAILABLE: {self.available}
TYPE: {self.type}
*****'''
