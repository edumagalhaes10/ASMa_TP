import random
import time
import asyncio

class LandingTrack:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.available = True

    def get_coords(self):
        return self.x, self.y

    def get_available(self):
        return self.available
    

    # def timer_available(self):
    #     asyncio.sleep(2)
    #     self.available = True

    def set_available(self, availability):
        self.available = availability
        # if availability == False:
        #     self.timer_available()
