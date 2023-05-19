import random

class Hangar:
    def __init__(self, type, hangar_id):
        self.hangar_id = hangar_id
        self.x = "%.2f" % random.uniform(-100, 100)
        self.y = "%.2f" % random.uniform(-100, 100)
        self.available = True
        self.type = type
        self.plane = None

    def get_id(self):
        return self.hangar_id

    def get_coords(self):
        return self.x, self.y

    def get_availability(self):
        return self.available

    def set_plane(self, plane):
        self.available = False
        self.plane = plane

    def remove_plane(self):
        self.available = True
        self.plane = None

    def __str__(self):
        return f'''Hangar Id: {self.hangar_id} | X: {self.x} | Y: {self.y}'''
        # return f'''***** HANGAR: Hangar Id: {self.hangar_id} | X: {self.x} | Y: {self.y} | AVAILABLE: {self.available} | TYPE: {self.type} | Plane: {self.plane} *****'''
