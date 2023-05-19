
class LandingTrack:
    def __init__(self, x, y, id):
        self.id = f"Landing Track {id}"
        self.x = x
        self.y = y
        self.available = True
        self.plane = None
        self.state_plane = None

    def get_id(self):
        return self.id
    
    def get_plane(self):
        return self.plane

    def get_state_plane(self):
        return self.state_plane

    def get_coords(self):
        return self.x, self.y

    def get_available(self):
        return self.available
    
    def set_available(self, availability):
        self.available = availability

    def set_plane(self, plane, state):
        self.plane = plane
        self.state_plane = state

    def remove_plane(self):
        self.plane = None
        self.state_plane = None
