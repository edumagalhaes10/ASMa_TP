
class LandingTrack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = True

    def get_coords(self):
        return self.x, self.y

    def get_available(self):
        return self.available
    
    def set_available(self, availability):
        self.available = availability
