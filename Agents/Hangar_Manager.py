from spade.agent import Agent
from UtilsAirport.Hangar import Hangar
from Behaviours.InformControlTower import InformControlTower
from Behaviours.HangarManagerListener import HangarManagerListener

class Hangar_Manager(Agent):
    async def setup(self):
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("hangars", [])
        self.set("max_hangars", 20)
        self.set("Commercial_hangars", 10)
        self.set("Cargo_hangars",10)
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
                    elif ( (pow(float(xy[0])- float(hangar.x),2) + pow(float(xy[1])- float(hangar.y),2)) < (pow(float(xy[0])- float(hangar_available.x),2) + pow(int(xy[1])- float(hangar_available.y),2))):
                        hangar_available = hangar
                        track = id_track

        if hangar_available != None:
            hangar_available.set_plane(plane)
        print("FREAKING OUT : ", track, hangar_available)
        return track, hangar_available


    def add_plane_to_hangar(self, type, plane):
        for hangar in self.get("hangars"):
            if type == hangar.type and hangar.available == True:
                hangar.set_plane(plane)
                return hangar
        
    def remove_plane_from_hangar(self,plane):
        for hangar in self.get("hangars"):
            if plane == hangar.plane:
                hangar.remove_plane()



        
