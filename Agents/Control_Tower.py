from spade.agent import Agent
from Behaviours.ConfirmTakeOff import ConfirmTakeOff
from Behaviours.ConfirmLanding import ConfirmLanding
from UtilsAirport.LandingTrack import LandingTrack
from Behaviours.ControlTowerListener import ControlTowerListener


class Control_Tower(Agent):
    
    async def setup(self):
        print(f"Control Tower {str(self.jid)}" + " starting...")
        self.set("landingQueue", [])
        self.set("takeOffQueue",[])
        self.set("planeInOperation", ("",""))
        self.set("maxPlanes2Land", 10)
        landingTrack = LandingTrack()
        self.set("landingTrack", landingTrack)
        #SECALHAR JUNTAR ESTES DOIS BEHAVIOURS
        c = ControlTowerListener()
        c = self.add_behaviour(c)
        a = ConfirmTakeOff()  
        self.add_behaviour(a)
        b = ConfirmLanding()
        self.add_behaviour(b)
