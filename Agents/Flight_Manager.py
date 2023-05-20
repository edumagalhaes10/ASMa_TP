from spade.agent import Agent
from Behaviours.AskFlightInfo import AskFlightInfo
from Behaviours.FlightManagerListener import FlightManagerListener

class Flight_Manager(Agent):

    async def setup(self):
        print(f"Hangar Manager {str(self.jid)}" + " starting...")
        self.set("Queue",[])
        
                
        a = AskFlightInfo(period=2)
        self.add_behaviour(a)

        b = FlightManagerListener()
        self.add_behaviour(b)
    