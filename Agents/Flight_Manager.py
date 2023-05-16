from spade.agent import Agent
from Behaviours.AskFlightInfo import AskFlightInfo
from Behaviours.FlightManagerListener import FlightManagerListener

class Flight_Manager(Agent):
    """ * plane landing
        * plane taking off
        * Fila de espera para aterrar
        * Fila de espera para descolar
    """
    async def setup(self):
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("planeInOperation", ("",""))
        self.set("Queue",[])
        # self.set("landingQueue", [])
        # self.set("takeOffQueue",[])

                
        a = AskFlightInfo(period=2)
        self.add_behaviour(a)

        b = FlightManagerListener()
        self.add_behaviour(b)
    