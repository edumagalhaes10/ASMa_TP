from spade.agent import Agent
from UtilsAirport.Hangar import Hangar
from Behaviours.InformControlTower import InformControlTower
from Behaviours.HangarManagerListener import HangarManagerListener
import json

class Hangar_Manager(Agent):
    async def setup(self):
        f = open("conf.json")
        conf = json.load(f)
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("hangars", [])
        self.set("Commercial_hangars", conf["Commercial_hangars"])
        self.set("Cargo_hangars",conf["Cargo_hangars"])
        self.set("max_hangars",  self.get("Cargo_hangars") +  self.get("Commercial_hangars"))

        for i in range(self.get("max_hangars")):
            if i < self.get("Commercial_hangars"):
                hangar = Hangar("Commercial", f"hangar{i}")
                self.get("hangars").append(hangar)
            else:
                hangar = Hangar("Cargo", f"hangar{i}")
                self.get("hangars").append(hangar)
                
        a = InformControlTower()
        self.add_behaviour(a)
          
        b = HangarManagerListener()
        self.add_behaviour(b)
        
        # for i in range(16):
        #     print(self.get("hangars")[i].__str__())

    def closest_available(self, type, plane, available_tracks):
        hangar_available = None
        track = None
        for id_track, xy in available_tracks.items():
            for hangar in self.get("hangars"):
                if type == hangar.type and hangar.available == True:
                    if hangar_available == None: 
                        hangar_available = hangar
                        track = id_track
                    elif ( (pow(float(xy[0])- float(hangar.x),2) + pow(float(xy[1])- float(hangar.y),2)) < (pow(float(xy[0])- float(hangar_available.x),2) + pow(float(xy[1])- float(hangar_available.y),2))):
                        hangar_available = hangar
                        track = id_track

        if hangar_available != None:
            hangar_available.set_plane(plane)
        return track, hangar_available


    def add_plane_to_hangar(self, type, plane):
        for hangar in self.get("hangars"):
            # print("HANGAR ID =", hangar.get_id(), " | AVAILABLE = ", hangar.get_availability())
            if type == hangar.type and hangar.get_availability() == True:
                hangar.set_plane(plane)
                return hangar
        
    def remove_plane_from_hangar(self,plane):
        
        for hangar in self.get("hangars"):
            if plane == hangar.plane:
                hangar.remove_plane()



        
