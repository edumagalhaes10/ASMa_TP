from spade.agent import Agent
from UtilsAirport.Hangar import Hangar
from Behaviours.InformControlTower import InformControlTower
from Behaviours.HangarManagerListener import HangarManagerListener

class Hangar_Manager(Agent):
    async def setup(self):
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("hangars", [])
        self.set("max_hangars", 16)
        self.set("Commercial_hangars", 14)
        self.set("Cargo_hangars",2)
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

    def closest_available(self, type, plane):
        hangar_available = None
        for hangar in self.get("hangars"):
            if type == hangar.type and hangar.available == True:
                if hangar_available == None: 
                    hangar_available = hangar
                elif (hangar.x + hangar.y) < (hangar_available.x + hangar_available.y):
                    hangar_available = hangar
        
        if hangar_available != None:
            hangar_available.set_plane(plane)
        return hangar_available


    def add_plane_to_hangar(self, type, plane):
        for hangar in self.get("hangars"):
            if type == hangar.type and hangar.available == True:
                hangar.set_plane(plane)



        
