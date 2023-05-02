from spade.agent import Agent
from UtilsAirport.Hangar import Hangar
from Behaviours.InformControlTower import InformControlTower

class Hangar_Manager(Agent):
    async def setup(self):
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("hangars", [])
        self.set("max_hangars", 16)
        self.set("comercial_hangars", 14)
        self.set("cargo_hangars",2)
        for i in range(self.get("max_hangars")):
            if i < self.get("comercial_hangars"):
                hangar = Hangar("comercial")
                self.get("hangars").append(hangar)
            else:
                hangar = Hangar("cargo")
                self.get("hangars").append(hangar)
                
        a = InformControlTower()
        self.add_behaviour(a)

        
        # for i in range(16):
        #     print(self.get("hangars")[i].__str__())

    def closest_available(self, type):
        hangar_available = None
        for hangar in self.get("hangars"):
            if type == hangar.type and hangar.available == True:
                if hangar_available == None: 
                    hangar_available = hangar
                elif (hangar.x + hangar.y) < (hangar_available.x + hangar_available.y):
                    hangar_available = hangar
        
        return hangar_available




        
