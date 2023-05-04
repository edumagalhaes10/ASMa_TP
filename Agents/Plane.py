from spade.agent import Agent
from Behaviours.Permission2TakeOff import Permission2TakeOff
from Behaviours.PlaneListener import PlaneListener
from Behaviours.Permission2Land import Permission2Land


class Plane(Agent):

    companies = {1:"TAP", 2:"Ryanair", 3:"Aegean Airlines", 4:"AirBaltic", 5:"Air Europa", 6:"Air Transat", 7:"Azores Airlines", 8:"British Airways", 9:"Brussels Airlines", 10:"EasyJet", 11: "Eurowings", 12:"Finnair", 13:"Iberia", 14:"Lufthansa", 15:"Luxair", 16:"Transavia", 17:"Vueling", 18:"Wizz Air", 19:"KLM", 20:"Swiss International"}
    destinations = {} # adicionar alguns destinos

    def __str__(self):
        return f'''*****
PLANE {self.get("id")}
JID: {self.get("jid")}
COMPANY: {self.get("company")}
*****'''

    async def setup(self):
        print(f"Plane {str(self.jid)}" + " starting...")

        if self.get("status") == "permission2TakeOff":
            permission2TakeOff = Permission2TakeOff()
            self.add_behaviour(permission2TakeOff)
        elif self.get("status") == "permission2Land":
            permission2Land = Permission2Land()
            self.add_behaviour(permission2Land )

        b = PlaneListener()
        self.add_behaviour(b)

