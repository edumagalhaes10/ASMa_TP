import random

class LandingTrack:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.available = True

    def get_coords(self):
        return self.x, self.y

    def get_available(self):
        return self.available
    
    def set_available(self, availability):
        self.available = availability
